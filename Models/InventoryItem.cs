using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace AklanDrugstoreInventory.Models;

public class InventoryItem : INotifyPropertyChanged
{
    private string name = string.Empty;
    private string category = string.Empty;
    private int quantity;
    private decimal price;
    private DateTime expiryDate = DateTime.Today.AddYears(1);

    public Guid Id { get; set; }

    public string Name
    {
        get => name;
        set => SetField(ref name, value);
    }

    public string Category
    {
        get => category;
        set => SetField(ref category, value);
    }

    public int Quantity
    {
        get => quantity;
        set
        {
            if (SetField(ref quantity, value))
                OnPropertyChanged(nameof(ChartHeight));
        }
    }

    public decimal Price
    {
        get => price;
        set => SetField(ref price, value);
    }

    public DateTime ExpiryDate
    {
        get => expiryDate;
        set => SetField(ref expiryDate, value);
    }

    public double ChartHeight => Math.Clamp(Quantity * 5, 12, 160);

    public event PropertyChangedEventHandler? PropertyChanged;

    private bool SetField<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value))
            return false;

        field = value;
        OnPropertyChanged(propertyName);
        return true;
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
}
