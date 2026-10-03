using System.Collections.ObjectModel;
using System.Text.Json;
using AklanDrugstoreInventory.Models;

namespace AklanDrugstoreInventory;

public partial class MainPage : ContentPage
{
    private readonly string inventoryFile = Path.Combine(FileSystem.AppDataDirectory, "inventory.json");
    private readonly string auditFile = Path.Combine(FileSystem.AppDataDirectory, "audit.json");
    private InventoryItem? selectedItem;
    private bool dataLoaded;

    public ObservableCollection<InventoryItem> Items { get; } = [];
    public ObservableCollection<AuditEntry> AuditEntries { get; } = [];

    public MainPage()
    {
        InitializeComponent();
        BindingContext = this;
        ExpiryPicker.Date = DateTime.Today.AddYears(1);
    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        if (dataLoaded)
            return;

        dataLoaded = true;
        await LoadDataAsync();
        UpdateDashboard();
    }

    private void OnLoginClicked(object? sender, EventArgs e)
    {
        if (UsernameEntry.Text?.Trim().Equals("admin", StringComparison.OrdinalIgnoreCase) == true &&
            PasswordEntry.Text == "admin123")
        {
            LoginMessage.IsVisible = false;
            LoginPanel.IsVisible = false;
            AppPanel.IsVisible = true;
            AddAudit("LOGIN", "Local administrator logged in.");
            ShowPanel(DashboardPanel);
            return;
        }

        LoginMessage.Text = "Incorrect username or password.";
        LoginMessage.IsVisible = true;
    }

    private void OnLogoutClicked(object? sender, EventArgs e)
    {
        AddAudit("LOGOUT", "Local administrator logged out.");
        PasswordEntry.Text = string.Empty;
        AppPanel.IsVisible = false;
        LoginPanel.IsVisible = true;
    }

    private void OnDashboardMenuClicked(object? sender, EventArgs e) => ShowPanel(DashboardPanel);
    private void OnInventoryMenuClicked(object? sender, EventArgs e) => ShowPanel(InventoryPanel);
    private void OnAuditMenuClicked(object? sender, EventArgs e) => ShowPanel(AuditPanel);

    private void ShowPanel(VisualElement panel)
    {
        DashboardPanel.IsVisible = panel == DashboardPanel;
        InventoryPanel.IsVisible = panel == InventoryPanel;
        AuditPanel.IsVisible = panel == AuditPanel;
        UpdateDashboard();
    }

    private async void OnAddClicked(object? sender, EventArgs e)
    {
        if (!TryReadForm(out string name, out string category, out int quantity, out decimal price))
            return;

        var item = new InventoryItem
        {
            Id = Guid.NewGuid(),
            Name = name,
            Category = category,
            Quantity = quantity,
            Price = price,
            ExpiryDate = ExpiryPicker.Date ?? DateTime.Today
        };

        Items.Add(item);
        AddAudit("ADD", $"Added {item.Name} with {item.Quantity} unit(s).");
        await SaveDataAsync();
        ClearForm();
        UpdateDashboard();
    }

    private async void OnUpdateClicked(object? sender, EventArgs e)
    {
        if (selectedItem is null)
        {
            ShowFormError("Select a product to update.");
            return;
        }

        if (!TryReadForm(out string name, out string category, out int quantity, out decimal price))
            return;

        string oldName = selectedItem.Name;
        selectedItem.Name = name;
        selectedItem.Category = category;
        selectedItem.Quantity = quantity;
        selectedItem.Price = price;
        selectedItem.ExpiryDate = ExpiryPicker.Date ?? DateTime.Today;

        AddAudit("UPDATE", $"Updated {oldName} to {selectedItem.Name} ({selectedItem.Quantity} unit(s)).");
        await SaveDataAsync();
        ClearForm();
        UpdateDashboard();
    }

    private async void OnDeleteClicked(object? sender, EventArgs e)
    {
        if (selectedItem is null)
        {
            ShowFormError("Select a product to delete.");
            return;
        }

        bool confirmed = await DisplayAlertAsync("Delete product", $"Remove {selectedItem.Name}?", "Delete", "Cancel");
        if (!confirmed)
            return;

        string productName = selectedItem.Name;
        Items.Remove(selectedItem);
        AddAudit("DELETE", $"Deleted {productName}.");
        await SaveDataAsync();
        ClearForm();
        UpdateDashboard();
    }

    private void OnClearClicked(object? sender, EventArgs e) => ClearForm();

    private void OnInventorySelectionChanged(object? sender, SelectionChangedEventArgs e)
    {
        selectedItem = e.CurrentSelection.FirstOrDefault() as InventoryItem;
        if (selectedItem is null)
            return;

        NameEntry.Text = selectedItem.Name;
        CategoryEntry.Text = selectedItem.Category;
        QuantityEntry.Text = selectedItem.Quantity.ToString();
        PriceEntry.Text = selectedItem.Price.ToString("0.00");
        ExpiryPicker.Date = selectedItem.ExpiryDate;
        FormMessage.IsVisible = false;
    }

    private bool TryReadForm(out string name, out string category, out int quantity, out decimal price)
    {
        name = NameEntry.Text?.Trim() ?? string.Empty;
        category = CategoryEntry.Text?.Trim() ?? string.Empty;
        bool quantityOk = int.TryParse(QuantityEntry.Text, out quantity) && quantity >= 0;
        bool priceOk = decimal.TryParse(PriceEntry.Text, out price) && price >= 0;

        if (string.IsNullOrWhiteSpace(name) || string.IsNullOrWhiteSpace(category) || !quantityOk || !priceOk)
        {
            ShowFormError("Enter a name, category, valid quantity, and valid price.");
            return false;
        }

        FormMessage.IsVisible = false;
        return true;
    }

    private void ShowFormError(string message)
    {
        FormMessage.Text = message;
        FormMessage.IsVisible = true;
    }

    private void ClearForm()
    {
        selectedItem = null;
        InventoryView.SelectedItem = null;
        NameEntry.Text = string.Empty;
        CategoryEntry.Text = string.Empty;
        QuantityEntry.Text = string.Empty;
        PriceEntry.Text = string.Empty;
        ExpiryPicker.Date = DateTime.Today.AddYears(1);
        FormMessage.IsVisible = false;
    }

    private void UpdateDashboard()
    {
        ProductCountLabel.Text = Items.Count.ToString();
        UnitCountLabel.Text = Items.Sum(item => item.Quantity).ToString();
        LowStockCountLabel.Text = Items.Count(item => item.Quantity <= 10).ToString();
    }

    private void AddAudit(string action, string details)
    {
        AuditEntries.Insert(0, new AuditEntry
        {
            Time = DateTime.Now,
            Action = action,
            Details = details
        });

        _ = SaveAuditAsync();
    }

    private async Task LoadDataAsync()
    {
        try
        {
            if (File.Exists(inventoryFile))
            {
                string json = await File.ReadAllTextAsync(inventoryFile);
                foreach (InventoryItem item in JsonSerializer.Deserialize<List<InventoryItem>>(json) ?? [])
                    Items.Add(item);
            }

            if (File.Exists(auditFile))
            {
                string json = await File.ReadAllTextAsync(auditFile);
                foreach (AuditEntry entry in JsonSerializer.Deserialize<List<AuditEntry>>(json) ?? [])
                    AuditEntries.Add(entry);
            }
        }
        catch
        {
            // A damaged local file should not prevent the student demo from opening.
        }

        if (Items.Count == 0)
        {
            Items.Add(new InventoryItem { Id = Guid.NewGuid(), Name = "Paracetamol 500mg", Category = "Medicine", Quantity = 25, Price = 5.50m, ExpiryDate = DateTime.Today.AddYears(2) });
            Items.Add(new InventoryItem { Id = Guid.NewGuid(), Name = "Vitamin C", Category = "Vitamins", Quantity = 18, Price = 8.00m, ExpiryDate = DateTime.Today.AddYears(1) });
            Items.Add(new InventoryItem { Id = Guid.NewGuid(), Name = "Alcohol 70%", Category = "First Aid", Quantity = 9, Price = 45.00m, ExpiryDate = DateTime.Today.AddMonths(18) });
            Items.Add(new InventoryItem { Id = Guid.NewGuid(), Name = "Face Mask", Category = "Supplies", Quantity = 32, Price = 3.00m, ExpiryDate = DateTime.Today.AddYears(3) });
            await SaveDataAsync();
        }
    }

    private async Task SaveDataAsync()
    {
        string json = JsonSerializer.Serialize(Items, new JsonSerializerOptions { WriteIndented = true });
        await File.WriteAllTextAsync(inventoryFile, json);
    }

    private async Task SaveAuditAsync()
    {
        string json = JsonSerializer.Serialize(AuditEntries, new JsonSerializerOptions { WriteIndented = true });
        await File.WriteAllTextAsync(auditFile, json);
    }
}
