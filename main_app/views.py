import json
import csv
import io
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import IntegrityError
from .forms import UnifiedUserForm
from .models import UserProfile, Address, ShippingAndTax

# --- Helper: Convert form errors to JSON ---
def get_form_errors_json(form_errors):
    return {field: [str(e) for e in errors] for field, errors in form_errors.items()}

# ---------------------------------------------------

def home_page(request):
    form = UnifiedUserForm()

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # --- Normal form submission ---
        form = UnifiedUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # --- 1. Create UserProfile ---
                user_profile = UserProfile.objects.create(
                    Name=data['Name'],
                    Mobile=data.get('Mobile', ''),
                    Email=data.get('Email', ''),
                    Group=data.get('Group', ''),
                    Status=data.get('Status', ''),
                    Active=data.get('Active', True),
                    CreditLimit=data.get('CreditLimit'),
                    PaymentTerms=data.get('PaymentTerms', ''),
                    Salesman=data.get('Salesman', ''),
                    DefaultPriority=data.get('DefaultPriority', 5),
                    AlertNotes=data.get('AlertNotes', ''),
                    QuickBooksClassName=data.get('QuickBooksClassName', ''),
                    IssuableStatus=data.get('IssuableStatus', ''),
                    Number=data.get('Number') or None
                )

                # --- 2. Create Primary Address ---
                address_record = Address.objects.create(
                    user=user_profile,
                    AddressName=data.get('AddressName', ''),
                    AddressContact=data.get('AddressContact', ''),
                    AddressType=data.get('AddressType', ''),
                    IsDefault=data.get('IsDefault', False),
                    Address=data.get('Address', ''),
                    City=data.get('City', ''),
                    State=data.get('State', ''),
                    Zip=data.get('Zip', ''),
                    Country=data.get('Country', ''),
                    Fax=data.get('Fax', ''),
                    Pager=data.get('Pager', ''),
                    Web=data.get('Web', '')
                )

                # --- 3. Create ShippingAndTax ---
                ShippingAndTax.objects.create(
                    user=user_profile,
                    TaxRate=data.get('TaxRate'),
                    TaxExempt=data.get('TaxExempt', False),
                    TaxExemptNumber=data.get('TaxExemptNumber', ''),
                    URL=data.get('URL', ''),
                    CarrierName=data.get('CarrierName', ''),
                    CarrierService=data.get('CarrierService', ''),
                    ShippingTerms=data.get('ShippingTerms', ''),
                    ToBeEmailed=data.get('ToBeEmailed', False),
                    ToBePrinted=data.get('ToBePrinted', False),
                )

                # --- 4. Return success JSON ---
                return JsonResponse({
                    'success': True,
                    'message': f'Customer "{user_profile.Name}" saved successfully.',
                    'new_record': {
                        'id': user_profile.pk,
                        'LocationName': user_profile.Name,
                        'Address': address_record.Address,
                        'City': address_record.City,
                        'State': address_record.State,
                        'Zip': address_record.Zip,
                        'ContactPerson': address_record.AddressContact,
                        'Phone': user_profile.Mobile,
                        'Email': user_profile.Email,
                    }
                }, status=201)

            except IntegrityError as e:
                error_message = f"Database error: {e}"
                if 'unique constraint' in str(e).lower() and 'number' in str(e).lower():
                    error_message = "Account Number already exists."
                return JsonResponse({'success': False, 'message': error_message, 'errors': {'Number': [error_message]}}, status=400)

            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Server error: {str(e)}', 'errors': 'Check server logs.'}, status=500)

        else:
            # Form invalid
            return JsonResponse({
                'success': False,
                'message': 'Form validation failed.',
                'errors': get_form_errors_json(form.errors),
            }, status=400)

    # --- GET request: render page with initial table data ---
    all_users = UserProfile.objects.all().prefetch_related('addresses').select_related('shipping_tax')
    initial_table_data = []
    for user in all_users:
        address = user.addresses.first()
        initial_table_data.append({
            'id': user.pk,
            'LocationName': user.Name,
            'Address': address.Address if address else '',
            'City': address.City if address else '',
            'State': address.State if address else '',
            'Zip': address.Zip if address else '',
            'ContactPerson': address.AddressContact if address else '',
            'Phone': user.Mobile,
            'Email': user.Email,
        })

    context = {
        'unified_form': form,
        'initial_table_data_json': json.dumps(initial_table_data)
    }
    return render(request, 'index.html', context)


# --- Export users to CSV ---
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_data.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Group', 'Account Number', 'Mobile', 'Email', 'Status', 'Credit Limit', 'Payment Terms',
        'Salesman', 'Priority', 'Alert Notes',
        'Address Name', 'Address Contact', 'Address Type', 'Address', 'City', 'State', 'Zip', 'Country',
        'Tax Rate', 'Tax Exempt', 'Tax Exempt Number', 'URL', 'Carrier', 'Shipping Terms',
        'Is Default', 'Active'
    ])

    users = UserProfile.objects.all().prefetch_related('addresses').select_related('shipping_tax')

    for user in users:
        address = user.addresses.first()
        shipping = getattr(user, 'shipping_tax', None)
        writer.writerow([
            user.Name,
            user.Group,
            user.Number or '',
            user.Mobile,
            user.Email,
            user.Status,
            user.CreditLimit or '',
            user.PaymentTerms,
            user.Salesman,
            user.DefaultPriority or '',
            user.AlertNotes or '',

            address.AddressName if address else '',
            address.AddressContact if address else '',
            address.AddressType if address else '',
            address.Address if address else '',
            address.City if address else '',
            address.State if address else '',
            address.Zip if address else '',
            address.Country if address else '',

            shipping.TaxRate if shipping else '',
            shipping.TaxExempt if shipping else False,
            shipping.TaxExemptNumber if shipping else '',
            shipping.URL if shipping else '',
            shipping.CarrierName if shipping else '',
            shipping.ShippingTerms if shipping else '',

            address.IsDefault if address else False,
            user.Active,
        ])
    return response


# --- Import users from CSV ---
def import_users_csv(request):
    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'success': False, 'message': 'File is not CSV type.'}, status=400)
        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            new_records = []

            for row in reader:
                # Create UserProfile
                user_profile = UserProfile.objects.create(
                    Name=row.get('Name', ''),
                    Mobile=row.get('Mobile', ''),
                    Email=row.get('Email', ''),
                    Group=row.get('Group', ''),
                    Status=row.get('Status', ''),
                    Active=row.get('Active', 'True') == 'True',
                    CreditLimit=row.get('Credit Limit') or None,
                    PaymentTerms=row.get('Payment Terms', ''),
                    Salesman=row.get('Salesman', ''),
                    DefaultPriority=row.get('Priority') or 5,
                    AlertNotes=row.get('Alert Notes', ''),
                    QuickBooksClassName='',
                    IssuableStatus='',
                    Number=row.get('Account Number') or None
                )

                # Create Address
                address_record = Address.objects.create(
                    user=user_profile,
                    AddressName=row.get('Address Name', ''),
                    AddressContact=row.get('Address Contact', ''),
                    AddressType=row.get('Address Type', ''),
                    IsDefault=row.get('Is Default', 'False') == 'True',
                    Address=row.get('Address', ''),
                    City=row.get('City', ''),
                    State=row.get('State', ''),
                    Zip=row.get('Zip', ''),
                    Country=row.get('Country', ''),
                    Fax='',
                    Pager='',
                    Web=''
                )

                # Create ShippingAndTax
                ShippingAndTax.objects.create(
                    user=user_profile,
                    TaxRate=row.get('Tax Rate') or None,
                    TaxExempt=row.get('Tax Exempt', 'False') == 'True',
                    TaxExemptNumber=row.get('Tax Exempt Number', ''),
                    URL=row.get('URL', ''),
                    CarrierName=row.get('Carrier', ''),
                    CarrierService='',
                    ShippingTerms=row.get('Shipping Terms', ''),
                    ToBeEmailed=False,
                    ToBePrinted=False,
                )

                new_records.append({
                    'id': user_profile.pk,
                    'LocationName': user_profile.Name,
                    'Address': address_record.Address,
                    'City': address_record.City,
                    'State': address_record.State,
                    'Zip': address_record.Zip,
                    'ContactPerson': address_record.AddressContact,
                    'Phone': user_profile.Mobile,
                    'Email': user_profile.Email,
                })

            return JsonResponse({'success': True, 'message': f'{len(new_records)} users imported successfully.', 'new_records': new_records})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error reading CSV: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)
