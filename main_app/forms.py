from django import forms

class UnifiedUserForm(forms.Form):
    # --- 1. USER PROFILE FIELDS ---
    Name = forms.CharField(max_length=255)

    # --- 2. ADDRESS FIELDS ---
    AddressName = forms.CharField(max_length=255, help_text="e.g., 'Primary Shipping', 'Billing'")
    AddressContact = forms.CharField(max_length=255, required=False)
    AddressType = forms.CharField(max_length=100, required=False)
    IsDefault = forms.BooleanField(required=False, initial=False)
    Address = forms.CharField(max_length=255)
    City = forms.CharField(max_length=100)
    State = forms.CharField(max_length=100)
    Zip = forms.CharField(max_length=20)
    Country = forms.CharField(max_length=100)

    # --- 3. CONTACT / PHONE / COMMUNICATION FIELDS ---
    Residential = forms.BooleanField(required=False, initial=False)
    Main = forms.CharField(max_length=20, required=False)
    Home = forms.CharField(max_length=20, required=False)
    Work = forms.CharField(max_length=20, required=False)
    Mobile = forms.CharField(max_length=20, required=False)
    Fax = forms.CharField(max_length=20, required=False)
    Email = forms.EmailField(max_length=254, required=False)
    Pager = forms.CharField(max_length=20, required=False)
    Web = forms.URLField(required=False)
    Other = forms.CharField(max_length=100, required=False)

    # --- 4. USER PROFILE CONTINUED ---
    Group = forms.CharField(max_length=100, required=False)
    CreditLimit = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.00, required=False)
    Status = forms.CharField(max_length=100, required=False, help_text="e.g., 'Normal'")
    Active = forms.BooleanField(required=False, initial=True)

    # --- 5. SHIPPING AND TAX FIELDS ---
    TaxRate = forms.DecimalField(max_digits=5, decimal_places=3, initial=0.000, required=False)
    Salesman = forms.CharField(max_length=150, required=False)
    DefaultPriority = forms.IntegerField(initial=5, required=False)
    Number = forms.CharField(max_length=50, required=False)
    PaymentTerms = forms.CharField(max_length=100, required=False)
    TaxExempt = forms.BooleanField(required=False, initial=False)
    TaxExemptNumber = forms.CharField(max_length=100, required=False)
    URL = forms.URLField(required=False)
    CarrierName = forms.CharField(max_length=100, required=False)
    CarrierService = forms.CharField(max_length=100, required=False)
    ShippingTerms = forms.CharField(max_length=100, required=False)

    # --- 6. NOTES AND SETTINGS ---
    AlertNotes = forms.CharField(widget=forms.Textarea, required=False)
    QuickBooksClassName = forms.CharField(max_length=255, required=False)
    ToBeEmailed = forms.BooleanField(required=False, initial=False)
    ToBePrinted = forms.BooleanField(required=False, initial=False)
    IssuableStatus = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define field order explicitly for consistent rendering
        self.order_fields([
            'Name',

            'AddressName', 'AddressContact', 'AddressType', 'IsDefault',
            'Address', 'City', 'State', 'Zip', 'Country',

            'Residential', 'Main', 'Home', 'Work', 'Mobile', 'Fax',
            'Email', 'Pager', 'Web', 'Other',

            'Group', 'CreditLimit', 'Status', 'Active',

            'TaxRate', 'Salesman', 'DefaultPriority', 'Number', 'PaymentTerms',
            'TaxExempt', 'TaxExemptNumber', 'URL', 'CarrierName', 'CarrierService', 'ShippingTerms',

            'AlertNotes', 'QuickBooksClassName', 'ToBeEmailed', 'ToBePrinted', 'IssuableStatus',
        ])

    # --- 7. CLEAN METHOD TO HANDLE EMPTY NUMERIC FIELDS ---
    def clean(self):
        """
        Converts empty strings in numeric fields to None (NULL).
        """
        cleaned_data = super().clean()
        numeric_fields = ['CreditLimit', 'TaxRate', 'DefaultPriority']
        for field_name in numeric_fields:
            value = cleaned_data.get(field_name)
            if value in [None, '']:
                cleaned_data[field_name] = None
        return cleaned_data
