from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_subject = f"Контактна форма: {subject}"
            email_message = f"""Нове повідомлення з контактної форми
            Від: {name}
            Email: {email}
            Тема: {subject}
            Повідомлення:{message}"""

            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Ваше повідомлення успішно відправлено! Дякуємо.')
                return redirect('contact:success')
            except BadHeaderError:
                messages.error(request, 'Помилка заголовка. Спробуйте ще раз.')
            except Exception as e:
                messages.error(request, 'Помилка відправки. Спробуйте пізніше.')
                if settings.DEBUG:
                    print(f"Email error: {e}")
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = ContactForm()

    return render(request, 'contact/contact_form.html', {'form': form})


def contact_success_view(request):
    return render(request, 'contact/success.html')