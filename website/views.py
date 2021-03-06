# -*- coding: utf-8 -*-

from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_backends
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.db.models.query_utils import Q
from django.template.defaultfilters import linebreaksbr
from django.utils import simplejson as json
from django.forms.models import ModelForm, ModelChoiceField
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.encoding import force_unicode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from configuration import configuration
from places.countries import  COUNTRIES_DICT
#from places.models import *
from places.models import Place, Profile, Currency, Tag, Description, Photo, TagTranslation, send_message
from places.options import n_tuple, PLACE_TYPES, SPACE_TYPES, DJSTRANS
from utils.htmlmail import send_html_mail
from website.models import Sayfa, Haber, Vitrin, Question, MiniVitrin
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from  django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer
from django.contrib import auth
from django.contrib import messages
import logging
from website.models.dil import __
from django.contrib.sessions.models import Session

log = logging.getLogger('genel')
noOfBeds=n_tuple(7)
placeTypes = [(0,_(u'All'))] + PLACE_TYPES

class SearchForm(forms.Form):
    checkin = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}),required=False, label=_('Check-in'))
    checkout = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}),required=False, label=_('Check-out'))
    query = forms.CharField(widget=forms.TextInput(), label=_(u'City or address'),required=False)
    no_of_guests = forms.ChoiceField(choices=noOfBeds, initial=1, label=_(u'Guests'),required=False)
    placeType = forms.ChoiceField(choices=placeTypes,required=False)

class BookingForm(forms.Form):
    checkin = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    checkout = forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))


    def __init__(self, capacity, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
#        log.info('cpapa %s'%n_tuple(capacity))
        self.fields['no_of_guests']= forms.ChoiceField(choices=n_tuple(capacity or 30), initial=1)


def place_translation(request, id, lang):
    trans = Place.c_get_translation(id, lang)
    return HttpResponse(json.dumps((linebreaksbr(trans[0],True),trans[1])), mimetype='application/json')

def showPlace(request, id):
    try:
        place = Place.objects.get(pk=id,active=True)
    except Place.DoesNotExist:
        raise Http404
#    owner = place.owner
#    profile = owner.profile
    properties=[
        (_(u'Place type'),place.get_type_display()),
        (_(u'Space offered'),place.get_space_display()),
        (_(u'Accommodates'),place.capacity),
        (_(u'Size'), place.get_size()  ),
        (_(u'Bedrooms'),place.bedroom),
        (_(u'Bed type'),place.get_bed_type_display()),
        (_(u'Bathrooms'),place.bathrooms),
        (_(u'Cancellation'),place.get_cancellation_display()),
    ]
#    if place.cleaning_fee:
#        properties.append((_(u'Cleaning Fee'),place.cleaning_fee))
    context = {'place':place, 'bform':BookingForm(place.max_stay),
               'properties':properties ,
#               'profile':profile,
               'service_fee':configuration('guest_fee'),
               'amens':place.getTags(request.LANGUAGE_CODE),
               'translations':place.get_translation_list(),
#               'other_places':Place.objects.filter(active=True, published=True, owner=profile.user).exclude(pk=place.id),
               'meta_keywords':place.title,
               'meta_desc':place.description,
               'page_title':place.title,
    }
    if request.LANGUAGE_CODE in place.get_translation_list():
        trns = place.get_translation(request.LANGUAGE_CODE)
        context['description'], context['title']  = trns
        context['meta_desc'] = trns[0]
        context['page_title'] = context['meta_keywords'] = trns[1]
    return render_to_response('show_place.html', context, context_instance=RequestContext(request))


def show_profile(request, id):
    profile = get_object_or_404(Profile,pk=id)
    places = Place.objects.filter(active=True, published=True, owner=profile.user)
    context = {'profile':profile, 'usr':profile.user,'places':places}
    return render_to_response('profile_page.html', context, context_instance=RequestContext(request))

def searchPlace(request):
    context = {}
    return render_to_response('search_place.html', context, context_instance=RequestContext(request))

class LoginForm(forms.Form):
    login_email = forms.EmailField(label=_(u'E-mail address'))
    login_pass = forms.CharField(widget=forms.PasswordInput(),label=_(u'Password'))

class RegisterForm(ModelForm):
    pass1 = forms.CharField(widget=forms.PasswordInput(),label=_(u'Password'))
    pass2 = forms.CharField(widget=forms.PasswordInput(),label=_(u'Password (Again)'))
    email = forms.EmailField(label=_(u'E-mail address'))
    class Meta:
        model=User
        fields = ('email','first_name','last_name',)

def anasayfa(request):
#    sayfa = Sayfa.al_anasayfa()
#    lang = request.LANGUAGE_CODE
    searchForm = SearchForm()
    slides = [Vitrin.get_slides(), Vitrin.get_slides(type=1), Vitrin.get_slides(type=2)]
    context = {'slides': slides,
               'minislides':MiniVitrin.get_slides(request.LANGUAGE_CODE),
               'srForm':searchForm,
               'nasil_slide_zaman': configuration('nasil_slide_zaman') or '0',

               }
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def slides(request, id):
    context = {'slides': Vitrin.get_slides(lang=request.LANGUAGE_CODE, type=int(id) or None), 'cachekey':'%s%s' %(request.LANGUAGE_CODE, id) }
    return render_to_response('slides.html', context, context_instance=RequestContext(request))

class addPlaceForm(ModelForm):
    lat= forms.FloatField(widget=forms.HiddenInput())
    lon= forms.FloatField(widget=forms.HiddenInput())
    currency = ModelChoiceField(Currency.objects.filter(active=True), empty_label=None)
    phone = forms.CharField(label=_('Your phone'))

#    neighborhood= forms.FloatField(widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):
        req_phone = kwargs.pop('req_phone',False)
        super(addPlaceForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()
        if not req_phone:
            del self.fields['phone']
#        self.fields['currency'].queryset = Currency.objects.filter(active=True)

    class Meta:
        model=Place
        fields = ('title','type','capacity','space','description','price','currency',
            'city','country','district','street','address','lat','lon','neighborhood','state',
            'postcode','tags', 'min_stay', 'max_stay', 'cancellation','manual','rules','size','size', 'size_type',
                  'bedroom'
            )


@login_required
def addPlace(request, ajax=False, id=None):
    template_name = "add_place_wizard.html" if ajax else "add_place.html"
    sayfa = Sayfa.al_anasayfa()
    lang = request.LANGUAGE_CODE
    user = request.user
    response = {}
    new_place = None
    loged_in = user.is_authenticated()
    photos = []
    profile = user.get_profile()
    ask_phone = not bool(profile.phone.strip()) if profile.phone else True
    if id:
        old_place = get_object_or_404(Place, pk=id)
        photos = list(old_place.photo_set.values_list('id',flat=True))
        if old_place.owner != request.user:
            return HttpResponseForbidden()
        old_place.invalidate_caches()
    else:
        old_place = Place()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        login_form = LoginForm(request.POST)
        form = addPlaceForm(request.POST, instance=old_place, req_phone=ask_phone)
        if form.is_valid():
            new_place=form.save(commit=False)
            new_place.translation_check()
#            if register_form.is_valid() or loged_in:
#                if not loged_in:
#                    user = register_form.save(commit=False)
#                    user.username = user.email
#                    user.set_password(register_form.cleaned_data['pass1'])
#                    user.save()
            phone = form.cleaned_data.get('phone')
            if phone:
                profile.phone = phone
                profile.save()
            new_place.owner = user
            new_place.lat = str(new_place.lat)
            new_place.lon = str(new_place.lon)
            new_place.lang = request.LANGUAGE_CODE
#            log.info('%s %s '% (new_place.lang, request.LANGUAGE_CODE))
            new_place.save()
            form.save_m2m()
            for tag in form.cleaned_data['tags']:
                new_place.tags.add(tag)
#            log.info(form.cleaned_data['tags'])

            new_place.save()
            d, new = Description.objects.get_or_create(place=new_place, lang=new_place.lang)
            d.text = new_place.description
            d.title = new_place.title
            d.save()
            tmp_photos = request.session.get('tmp_photos')
            if tmp_photos:
                Photo.objects.filter(id__in=tmp_photos).update(place=new_place)
                if tmp_photos[0]:
                    p=Photo.objects.filter(pk=tmp_photos[0])
                    if p: p[0].save()
                request.session['tmp_photos']=[]
            if not ajax:
                if not new_place.published:
                    messages.success(request, _('Your place succesfully saved but not published yet.'))
                    messages.info(request, _('You can publish this place by pressing the "Publish" button below.'))
                else:
                    messages.success(request, _('Your changes succesfully saved.'))
                return HttpResponseRedirect('%s#do_listPlaces,this'%reverse('dashboard'))
        else:
            for e in form.errors:
                messages.error(request, e)
        if ajax:
            response = {
                'user':getattr(user,'username'),
                'loged_in':loged_in,
#                'new_place':repr(new_place),
                'errors':form.errors,
                'new_place_id':getattr(new_place,'id',0),
            }
            return HttpResponse(json.dumps(response), mimetype='application/json')


    else:
        form = addPlaceForm(instance=old_place, req_phone=ask_phone)
        register_form = RegisterForm()
        login_form = LoginForm()
    str_fee =  _('%s Service Fee '% configuration('host_fee'))
    context = {'form':form, 'rform':register_form,'lform':login_form,'place':old_place,
               'host_fee':configuration('host_fee'), 'str_fee':str_fee, 'photos':photos,
               'tags':TagTranslation.objects.filter(lang=request.LANGUAGE_CODE),
               'existing_tags':[],

    }
    if id:
        context['existing_tags'] = old_place.tags.values_list('id',flat=True)
    return render_to_response(template_name, context, context_instance=RequestContext(request))


#def bannerxml(request, tip):
#    lang = request.LANGUAGE_CODE
#    context = {'slides': Vitrin.al_slide(banner_tip=tip, dilkodu=lang), }
#    ci = RequestContext(request)
#    return render_to_response('banner.xml', context, context_instance=ci)

#
#class IletisimForm(ModelForm):
#    class Meta:
#        model = Ileti
#        fields = ('gonderen_ad', 'gonderen_eposta', 'konu', 'yazi')
#
#
#def iletisim(request, urun_id=None):
#    lang = request.LANGUAGE_CODE
#    ilgili_urun_id = request.REQUEST.get('ilgili_urun')
#
##    urun = Urun.objects.get(pk=urun_id) if urun_id else None
#    urun = None
#    if request.method == 'POST':
#        form = IletisimForm(request.POST)
#        if form.is_valid():
#            i = form.save(commit=False)
#            i.ip = request.META.get('REMOTE_ADDR')
#
#            if urun:
#                tesk_msj='Ürünümüz hakkındaki mesajınız alındı. Teşekkür Ederiz.'
#                i.yazi = '%s adlı ürün hakkında;\n\n%s' % (urun.baslik(), i.yazi)
#            else:
#                tesk_msj='Mesajınız alındı. Teşekkür Ederiz.'
#            i.save()
#            messages.add_message(request, messages.INFO, tesk_msj)
#            return HttpResponseRedirect('/%s/mesaj_goster/'%lang)
#    else:
#        form = IletisimForm()
#        if urun:
#            form.fields['konu'].initial = urun.al_baslik(lang)
#    context = {'form': form,}
#    if urun:
#        context.update({'urun':urun,'icerik':urun.al_icerik(lang),
#                'kategoriler': urun.kategoriler(lang)})
#    elif request.GET.get('sayfa_id'):
#        context.update({'kategoriler':Sayfa.objects.get(pk=int(request.GET.get('sayfa_id'))).kategoriler(lang) })
#
#    ci = RequestContext(request)
#    return render_to_response('iletisim.html', context, context_instance=ci)


def icerik(request, id, slug):
    sayfa = get_object_or_404(Sayfa, pk=id)
    lang = request.LANGUAGE_CODE
    icerik = sayfa.al_icerik(lang)
    context = {'sayfa_id': sayfa.id, 'sayfa': sayfa,
               'icerik': icerik,
               'ust_baslik':sayfa.parent.al_baslik(lang) if sayfa.parent else '',
               'kategoriler': sayfa.yansayfalar(lang),
               'meta_keywords':icerik.tanim,
               'meta_desc':icerik.anahtar,
               'page_title':icerik.html_baslik,
               }
    ci = RequestContext(request)
    sablon = 'content_templates/' + (sayfa.sablon or 'icerik.html')
    return render_to_response(sablon, context, context_instance=ci)


def mesaj_goster(request):
    lang = request.LANGUAGE_CODE
    sayfa = Sayfa.al_anasayfa()
    context = {'sayfa': sayfa,'kategoriler': sayfa.kategoriler(lang)}
    ci = RequestContext(request)
    return render_to_response('content.html', context, context_instance=ci)


def haber_goster(request, id, slug):
    haber = get_object_or_404(Haber, pk=id)
    lang = request.LANGUAGE_CODE
    context = {'sayfa_id': haber.id, 'sayfa': haber,
               'icerik': {'metin': haber.icerik, 'baslik': haber.baslik},
               'kategoriler': haber.kategoriler(request.LANGUAGE_CODE)}
    ci = RequestContext(request)
    return render_to_response('content.html', context, context_instance=ci)


def dilsec(request, kod):
    url = request.GET.get('url')
    url = '/%s%s/' % (kod[:2], url[3:] if url else '/')
    return HttpResponseRedirect(url.replace('//', '/'))



@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
#        log.info('Called delete image. Photo id='+str(pk))
        image = get_object_or_404(Photo, pk=pk)
        if image.place and image.place.owner != request.user:
            return HttpResponseForbidden()
        image.delete()
#        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
#        log.info('Recieved not POST request todelete image view')
        return HttpResponseBadRequest('Only POST accepted')


def square_thumbnail(source, size=(50, 50)):
    thumbnail_options = dict(size=size, crop=True)
    return get_thumbnailer(source).get_thumbnail(thumbnail_options)

@csrf_exempt
def multiuploader(request, place_id=None):
    #FIXME : file type checking
    result = []
    if request.method == 'POST':
        if not request.FILES:
            return HttpResponseBadRequest('Must have files attached!')
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name[:59]
        file_size = wrapped_file.file.size
        image = Photo()
        image.name=filename
        image.image=file

        if place_id:
            place = get_object_or_404(Place, pk=place_id)
            if place.owner != request.user:
                return HttpResponseForbidden()
            image.place = place
        image.save()

        if not place_id:
            tmp_photos = request.session.get('tmp_photos',[])
            tmp_photos.append(image.id)
            request.session['tmp_photos'] = tmp_photos
        file_delete_url = '/delete_photo/'
        file_url = image.image.url
        result.append({"name":filename,
                       "size":file_size,
                       "url":file_url,
#                       "tag":thumb_tag,
#                       "turl":thumb_url,
                       "id":str(image.pk),
                       "delete_url":file_delete_url+str(image.pk),
                       "delete_type":"POST"})
    else:
        log.info('no POST request')
    response_data = json.dumps(result)
    return HttpResponse(response_data, mimetype='text/html')

@csrf_exempt
def bookmark(request):
    if request.method == 'POST':
        place =Place.objects.get(pk=request.POST.get('pid'))
        profile = request.user.get_profile()
        if request.POST.get('remove'):
            profile.favorites.remove(place)
            result = 'removed'
        else:
            profile.favorites.add(place)
            result = 'added'
        profile.save()
        return HttpResponse([result], mimetype='application/json')


@csrf_exempt
def send_message_to_host(request, data=None):
    if data is None:
        data = request.POST.copy()
    if data.get('message'):
        if not request.user.is_authenticated():
            request.session['message_to_host'] = request.POST.copy()
            result = {'message':force_unicode(_('Your message has saved.'))}
        else:
            send_message(request, data['message'], place=data['pid'])
            result = {'message':force_unicode(_('Your message successfully sent.'))}
        return HttpResponse(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@csrf_exempt
def set_message(request,msg):
    if request.method == 'POST':
        messages.info(request, DJSTRANS[msg])
    return HttpResponse([1], mimetype='application/json')


def image_view(request):
    items = Photo.objects.all()
    return render_to_response('images.html', {'items':items})

def statusCheck(request):
    context={
        'authenticated':request.user.is_authenticated(),
    }
    response =  HttpResponse(json.dumps(context), mimetype='application/json')
    response.set_cookie('lin', 1 if context['authenticated'] else -1)
    return response


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        rform = RegisterForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login_email'], password=form.cleaned_data['login_pass'])
            if user:
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                auth.login(request, user)
                request.user = user
                _do_post_login_jobs(request)
                response =  HttpResponseRedirect(request.POST.get('next') or reverse('dashboard') )
                response.set_cookie('ganibookmarks',
                    str(user.get_profile().favorites.values_list('id',flat=True) ))
                return response
            else:
                messages.error(request, _('Wrong email or password.'))
    else:
        form = LoginForm()
        rform = RegisterForm()
    context = {'form':form, 'rform':rform}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

def _do_post_login_jobs(request):
    if request.session.get('message_to_host'):
        send_message_to_host(request, request.session.get('message_to_host'))
        messages.success(request, _('Your message successfully sent.'))
        del request.session['message_to_host']

class UserAlreadyRegisteredError(Exception):
    pass

def register(request,template='register.html'):
    sayfa = Sayfa.al_anasayfa()
    lang = request.LANGUAGE_CODE
    user = request.user
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        lform = LoginForm(request.POST)
        if form.is_valid():
            try:
                if form.cleaned_data['pass1']==form.cleaned_data['pass2']:
                    if User.objects.filter(username = form.cleaned_data['email']):
                        raise UserAlreadyRegisteredError
                    user = form.save(commit=False)
                    user.username = user.email
                    user.set_password(form.cleaned_data['pass1'])
                    user.save()
                    user = auth.authenticate(username=user.email, password=form.cleaned_data['pass1'])
                    auth.login(request, user)
                    request.user = user
                    messages.success(request, _('Welcome to GaniHomes.'))

#                    send_message(request, __('hosgeldin mesaji',request.LANGUAGE_CODE), receiver=request.user, typ=40)
                    msg_context = {'user':user,
                                   'fullname':user.get_full_name(),
                                   'LANGUAGE_CODE':request.LANGUAGE_CODE}
                    send_html_mail(__('hosgeldin epostasi konu'),
                                    user.email,
                                    msg_context,
                                    template='mail/welcome_message.html',
                                    recipient_name=user.get_full_name())
                    _do_post_login_jobs(request)
                    return HttpResponseRedirect(request.POST.get('next') or reverse('dashboard') )
                else:
                    messages.error(request, _('The passwords you entered do not match.'))
            except UserAlreadyRegisteredError:
                messages.error(request, _('This email is already registered, please choose another one.'))
    else:
        form = RegisterForm()
        lform = LoginForm()
    context = {'form':form, 'lform':lform, 'next': request.GET.get('next','/')}
    return render_to_response(template, context, context_instance=RequestContext(request))


def registeration_thanks(request):
    context = {}
    return render_to_response('registeration_thanks.html', context, context_instance=RequestContext(request))

@csrf_exempt
def search(request):
    sresults = Place.objects.filter(published=True)
    form = SearchForm(request.REQUEST)
    lang = request.LANGUAGE_CODE
    amens = Tag.getTags(lang)
    context = {'form':form, 'amens':amens, 'place_types':PLACE_TYPES, 'space_types':SPACE_TYPES }
    return render_to_response('search.html', context, context_instance=RequestContext(request))


def parseJSData(request, key):
    data = request.POST.get(key)
    if data:
        return json.loads(data)
#        return [data] if type(data) not in (list, dict)  else data
    else:
        return []

@csrf_exempt
def search_ajax(request, current_page=1):
    form = SearchForm(request.REQUEST)
    pls = Place.objects.filter(published=True).distinct()
#    log.debug('search view')
#    pls = Place.objects.filter(q).values_list('neighborhood','district','city','state','country')
    if form.is_valid():
#        log.debug('search valid')
        query = form.cleaned_data['query']
        cin = form.cleaned_data['checkin']
        cout = form.cleaned_data['checkout']
        nog = form.cleaned_data['no_of_guests'] or 1
        pls = pls.filter(capacity__gte=nog)
    else:
        return HttpResponse(u'[]', mimetype='application/json')

    selected_currency = int(request.POST.get('scurrency', Currency.get_main_id()))
    min = int(request.REQUEST.get('pmin',0))
    max = int(request.REQUEST.get('pmax',1000))
    convert_factor = Currency.objects.get(pk=selected_currency).get_factor()
    if max < 500:
        max = max * convert_factor
        pls = pls.filter(gprice__lte=max)
    if min > 20:
        min = min * convert_factor
        pls = pls.filter(gprice__gte=min)
    amens = parseJSData(request,'ids_amens')
    if amens:
        for a in amens:
            pls = pls.filter(tags=a)
    stypes = parseJSData(request,'ids_stypes')
    if stypes:
        pls = pls.filter(space__in=stypes)
    ptypes = parseJSData(request,'ids_ptypes')
    if ptypes:
        pls = pls.filter(type__in=ptypes)
    if query:
        query = [q.strip() for q in query.split(',')[:2]]
#        log.debug('query: %s'%query)
        q = Q()
        for qp in query:
            q = q & Q(state__istartswith=qp) | Q(city__istartswith=qp) | Q(district__istartswith=qp) | Q(neighborhood__istartswith=qp) | Q(address__istartswith=qp)
        pls = pls.filter(q)
    if cin and cout:
        pls  = pls.filter(~Q(reserveddates__start__lte=cin, reserveddates__end__gte=cin) &
                          ~Q(reserveddates__start__gte=cout, reserveddates__end__lte=cout))
    paginator = Paginator(pls, 15)
    try:
        page = paginator.page(current_page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    resdict = json.dumps({
        'total':paginator.count,
        'has_next':page.has_next(),
        'has_previous':page.has_previous(),
        'numpages':paginator.num_pages,
        'current_page':current_page,
        'results':["PLACEHOLDER"],
    }, ensure_ascii=False)
    #adding our prepared/handcrafted search results
    resdict = resdict.replace('"PLACEHOLDER"', (u','.join(page.object_list.values_list('summary', flat=True))) )
    return HttpResponse(resdict, mimetype='application/json')

def cleandict(d):
     if not isinstance(d, dict):
         return d
     return dict((k,cleandict(v)) for k,v in d.iteritems() if v is not None)

def search_autocomplete(request):
    query = request.GET.get('q').split(' ')[:3]
    q = Q()
    for qp in query:
        q = q | Q(state__istartswith=qp) | Q(i18_tags__icontains=qp) | Q(district__istartswith=qp) | Q(neighborhood__istartswith=qp) | Q(address__istartswith=qp)
    places = set(list(Place.objects.filter(q).values_list('district','city','state','country').distinct()[:8]))
    nplaces = []
    for place in places:
        place = list(place)
        place[3] = force_unicode(COUNTRIES_DICT[place[3]])
        nplace = []
        for p in place:
            if not p: p = u''
            nplace.append(p)
#            log.info('type of %s : %s' % (p, type(p)))
        nplaces.append(nplace)
#    places = [filter(None,p) for p in places]
    return HttpResponse(json.dumps(nplaces,  ensure_ascii=False), mimetype='application/json')


def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    return render_to_response(template_name,
        context_instance = RequestContext(request)
    ) if not request.is_ajax() else HttpResponse('[]', mimetype='application/json')


def show_faqs(request):
    return render_to_response('faq.html',
            {'faq':Question.getFaqs(request.LANGUAGE_CODE)},
        context_instance=RequestContext(request))

from sqlprofiling import SqlProfilingMiddleware

def profiling(request):
    return render_to_response("profiling.html", {"queries": SqlProfilingMiddleware.Queries})

@staff_member_required
@never_cache
def user_from_session(request):
    session_key = request.GET.get('key')
    hata = ''
    try:
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        try:
            username = User.objects.filter(id=uid).values_list('username',flat=True)[0]
        except User.DoesNotExist:
            hata = 'kullanici bulunamadi'
    except Session.DoesNotExist:
        hata ='oturum bulunamadi'
    if not hata:
        return HttpResponseRedirect('/admin/places/profile/?q=%s'%username)
    else:
        return HttpResponse(hata, 'text/plain')



@staff_member_required
@never_cache
def matrix(request):
    """
    gercek admin istedigi musterinin hesabina girer cikar!
    """
    id=request.REQUEST.get('id')
    suser=request.user
    backend=get_backends()[0]
    backend="%s.%s" % (backend.__module__, backend.__class__.__name__)
    if request.user.is_superuser and id:
        musteri=User.objects.get(pk=id)
        if not musteri.is_superuser:
            musteri.backend=backend
            admin_id=request.user.id
#            log_it(admin_id,musteri, u'%s --> %s oldu!'%(request.user,musteri), kod=9)
            log.info('#%s %s kullanicisi #%s %s in yerine gecti.' % (suser.id, suser.username, id, musteri.username))
            auth.logout(request)
            auth.login(request, musteri)
            request.session['admin_id']=admin_id
        else:
            request.user.message_set.create(message=u'Super kullanici yerine geçmezsiniz!!!')
    else:
        request.user.message_set.create(message=u'Kimsenin yerine geçme yetkiniz yok!')
        return HttpResponseRedirect('/admin/places/profile/')
    return HttpResponseRedirect('/')
