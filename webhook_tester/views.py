from django.shortcuts import render


def webhook_tester(request):
    return render(request, "webhook_tester/webhook_test.html")
