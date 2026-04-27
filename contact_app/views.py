from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.contrib import messages

# Create your views here.

# Read (Display all contacts)
def contact_list(request):
    query = request.GET.get('q')
    
    if query:
        contacts = Contact.objects.filter(
            first_name__icontains=query
        ) | Contact.objects.filter(
            last_name__icontains=query
        ) | Contact.objects.filter(
            email__icontains=query
        )
    else:
        contacts = Contact.objects.all()

    return render(request, 'contact_list.html', {'contacts': contacts})

# Create new contact
from django.contrib import messages  # make sure this is at top

def contact_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # ✅ ADD THIS CHECK HERE
        if Contact.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('contact_create')

        # if no duplicate → save
        Contact.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            email=email,
            phone_number=request.POST.get('phone_number')
        )

        messages.success(request, "Contact added successfully")
        return redirect('contact_list')

    return render(request, 'contact_form.html')

# Update contact
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.first_name = request.POST.get('first_name')
        contact.last_name = request.POST.get('last_name')
        contact.address = request.POST.get('address')
        contact.email = request.POST.get('email')
        contact.phone_number = request.POST.get('phone_number')
        contact.save()
        messages.success(request, "Contact updated successfully")
        return redirect('contact_list')
    return render(request, 'contact_form.html', {'contact': contact})

# Delete contact
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "Contact deleted successfully")
    return redirect('contact_list')