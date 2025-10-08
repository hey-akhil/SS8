from django.db import models

# -----------------------
# 1. USER PROFILE
# -----------------------
class UserProfile(models.Model):
    Name = models.CharField(max_length=255)
    Mobile = models.CharField(max_length=20, blank=True, null=True)
    Email = models.EmailField(max_length=254, blank=True, null=True)
    Group = models.CharField(max_length=100, blank=True, null=True)
    Status = models.CharField(max_length=100, blank=True, null=True)
    Active = models.BooleanField(default=True)
    CreditLimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Number = models.CharField(max_length=50, blank=True, null=True)
    PaymentTerms = models.CharField(max_length=100, blank=True, null=True)
    Salesman = models.CharField(max_length=150, blank=True, null=True)
    DefaultPriority = models.IntegerField(null=True, blank=True)
    AlertNotes = models.TextField(blank=True, null=True)
    QuickBooksClassName = models.CharField(max_length=255, blank=True, null=True)
    IssuableStatus = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.Name

# -----------------------
# 2. ADDRESS
# -----------------------
class Address(models.Model):
    ADDRESS_TYPES = (
        ('RES', 'Residential'),
        ('MAIN', 'Main'),
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('OTHER', 'Other'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    AddressName = models.CharField(max_length=255)
    AddressContact = models.CharField(max_length=255, blank=True, null=True)
    AddressType = models.CharField(max_length=50, choices=ADDRESS_TYPES, blank=True, null=True)
    IsDefault = models.BooleanField(default=False)
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Zip = models.CharField(max_length=20)
    Country = models.CharField(max_length=100)
    Fax = models.CharField(max_length=20, blank=True, null=True)
    Pager = models.CharField(max_length=20, blank=True, null=True)
    Web = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.AddressName} ({self.user.Name})"

# -----------------------
# 3. SHIPPING AND TAX
# -----------------------
class ShippingAndTax(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='shipping_tax')
    TaxRate = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    TaxExempt = models.BooleanField(default=False)
    TaxExemptNumber = models.CharField(max_length=100, blank=True, null=True)
    URL = models.URLField(blank=True, null=True)
    CarrierName = models.CharField(max_length=100, blank=True, null=True)
    CarrierService = models.CharField(max_length=100, blank=True, null=True)
    ShippingTerms = models.CharField(max_length=100, blank=True, null=True)
    ToBeEmailed = models.BooleanField(default=False)
    ToBePrinted = models.BooleanField(default=False)

    def __str__(self):
        return f"Shipping & Tax for {self.user.Name}"
