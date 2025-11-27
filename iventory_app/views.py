from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
# django.views.genericからFormViewをインポート
from django.views.generic import FormView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからContactFormをインポート
from .forms import ContactForm
# django.contribからmessagesをインポート
from django.contrib import messages
# django.core.mailモジュールからEmailMessageをインポート
from django.core.mail import EmailMessage
from .models import Item
from .forms import ItemForm, SignUpForm, ContactForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# ------------------------------
# ユーザー登録・ログイン関連
# ------------------------------
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')  # 登録完了ページへリダイレクト
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def signup_success_view(request):
    return render(request, 'signup_success.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('item_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')


class MyLoginView(LoginView):
    template_name = 'login.html'


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('login')


# ------------------------------
# 在庫管理
# ------------------------------
@method_decorator(login_required, name='dispatch')
class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'


@method_decorator(login_required, name='dispatch')
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item_form.html'
    extra_context = {'title': '在庫追加'}


@method_decorator(login_required, name='dispatch')
class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'item_form.html'
    extra_context = {'title': '在庫編集'}


@method_decorator(login_required, name='dispatch')
class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('item_list')
    
class ContactView(FormView):
    '''問い合わせページを表示するビュー
    フォームで入力されたデータを取得し、メールの作成と送信を行う
    '''
    # contact.htmlをレンダリングする
    template_name='contact.html'
    # クラス変数form_classにforms.pyで定義したContactFormを設定
    form_class = ContactForm
    # 送信完了後にリダイレクトするページ
    success_url=reverse_lazy('countryapp:contact')

    def form_valid(self, form):
        '''
        FormViewクラスのform_valid()をオーバライド
        フォームのバリデーションを通過したデータがpostされたときに呼ばれる
        メール送信を行う
        parameters:
          form(object): ContactFormのオブジェクト
        Return:
          HttpResponseRedirectのオブジェクト
          オブジェクトをインスタンス化するとsuccess_urlで
          設定されているURLにリダイレクトされる
        '''
        # フォームに入力されたデータをフィールド名を指定して取得
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        # メールのタイトルの書式を設定
        subject ='お問い合わせ:{}'.format(title)
        # フォームの入力データの書式を設定
        message = \
          '送信者名:{0}\n メールアドレス:{1}\n タイトル:{2}\n メッセージ:{3}' \
          .format(name, email, title, message)
        # メールの送信元のアドレス
        from_email = 'admin@example.com'
        # 送信先のメールアドレス
        to_list = ['admin@example.com']
        # EmailMessageオブジェクトを生成
        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               )
        # EmailMessageクラスのsend()でメールサーバからメールを送信
        message.send()
        # 送信完了後に表示するメッセージ
        messages.success(
            self.request, 'お問い合わせは正常に送信されました。'
        )
        return super().form_valid(form)


# ------------------------------
# お問い合わせ
# ------------------------------
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # フォームのデータ取得
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_body = form.cleaned_data['message']

            # メール送信
            send_mail(
                subject=f'お問い合わせ: {name}',
                message=f'送信者: {name} <{email}>\n\n{message_body}',
                from_email=settings.CONTACT_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
            )

            messages.success(request, 'メッセージを送信しました！')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
