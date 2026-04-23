import numpy as np
from datetime import datetime
import csv
import os

class HotelFinanceSystem:
    def __init__(self):
        self.hotel_name = "SERENITY BY RCRG"
        self.rooms_file = "rooms_min_max.csv"
        self.room_types = None
        self.min_costs = None
        self.max_costs = None
        self.room_categories = None
        self.load_room_costs()
        
    def load_room_costs(self):
        """Load room costs with min-max pricing from CSV file"""
        try:
            room_types = []
            min_costs = []
            max_costs = []
            categories = []
            
            with open(self.rooms_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                
                for row in reader:
                    room_types.append(row[0].strip())
                    min_costs.append(float(row[1]))
                    max_costs.append(float(row[2]))
                    categories.append(row[3].strip() if len(row) > 3 else 'Standard')
            
            self.room_types = np.array(room_types)
            self.min_costs = np.array(min_costs)
            self.max_costs = np.array(max_costs)
            self.room_categories = np.array(categories)
            
            print(f"\n✓ Room pricing loaded successfully from {self.rooms_file}")
            print(f"  Total room types: {len(self.room_types)}")
            
        except FileNotFoundError:
            print(f"\n✗ Error: {self.rooms_file} not found!")
            print("Creating sample rooms_min_max.csv file...")
            self.create_sample_rooms_file()
            self.load_room_costs()
        except Exception as e:
            print(f"Error loading file: {e}")
            print("Creating new sample file...")
            self.create_sample_rooms_file()
            self.load_room_costs()
    
    def create_sample_rooms_file(self):
        """Create a sample rooms_min_max.csv file with min-max pricing"""
        sample_data = [
            ['Room Type', 'Min Price (₹)', 'Max Price (₹)', 'Category'],
            ['Standard Single', 2000, 3500, 'Economy'],
            ['Standard Double', 3000, 4500, 'Economy'],
            ['Deluxe Single', 4000, 6000, 'Premium'],
            ['Deluxe Double', 5000, 7000, 'Premium'],
            ['Suite', 8000, 12000, 'Luxury'],
            ['Premium Suite', 11000, 15000, 'Luxury'],
            ['Family Room', 6000, 9000, 'Premium'],
            ['Executive Room', 7000, 10000, 'Premium'],
            ['Presidential Suite', 15000, 25000, 'Luxury'],
            ['Garden View Room', 3500, 5500, 'Economy']
        ]
        
        with open(self.rooms_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(sample_data)
        
        print(f"✓ Sample {self.rooms_file} created successfully!")
    
    def calculate_dynamic_price(self, base_min, base_max):
        """Calculate dynamic pricing based on season and demand"""
        current_month = datetime.now().month
        
        # Seasonal multiplier array (12 months)
        seasonal_multiplier = np.array([
            0.8,  # Jan - Low
            0.9,  # Feb - Low
            1.0,  # Mar - Normal
            1.1,  # Apr - Peak
            1.2,  # May - Peak
            1.15, # Jun - Peak
            1.0,  # Jul - Normal
            0.9,  # Aug - Normal
            1.0,  # Sep - Normal
            1.1,  # Oct - Peak
            1.2,  # Nov - Peak
            1.3   # Dec - Super Peak (Holiday)
        ])
        
        season_factor = seasonal_multiplier[current_month - 1]
        
        # Weekend multiplier (Friday-Sunday)
        today_weekday = datetime.now().weekday()
        weekend_multiplier = 1.15 if today_weekday >= 4 else 1.0
        
        # Calculate final price (leaning towards max price in peak seasons)
        price_range = base_max - base_min
        dynamic_price = base_min + (price_range * (season_factor - 0.8) / 0.5)
        dynamic_price = np.clip(dynamic_price, base_min, base_max)
        
        # Apply weekend multiplier
        dynamic_price *= weekend_multiplier
        
        return round(dynamic_price, 2)
    
    def display_room_options(self, show_dynamic=True):
        """Display available room types with min-max and dynamic pricing"""
        print(f"\n{'='*70}")
        print(f"         {self.hotel_name}")
        print(f"{'='*70}")
        print("AVAILABLE ROOM TYPES & PRICING:")
        print("-" * 70)
        print(f"{'#':<3} {'Room Type':<22} {'Min':<10} {'Max':<10} {'Category':<12}", end="")
        if show_dynamic:
            print(f"{'Dynamic':<12}")
        else:
            print()
        print("-" * 70)
        
        for i in range(len(self.room_types)):
            dynamic_price = self.calculate_dynamic_price(self.min_costs[i], self.max_costs[i])
            
            print(f"{i+1:<3} {self.room_types[i]:<22} "
                  f"₹{self.min_costs[i]:>7,.0f}  ₹{self.max_costs[i]:>7,.0f}  "
                  f"{self.room_categories[i]:<12}", end="")
            if show_dynamic:
                print(f"₹{dynamic_price:>9,.0f}")
            else:
                print()
        print("-" * 70)
        
        if show_dynamic:
            current_month = datetime.now().strftime('%B')
            print(f"* Dynamic prices shown for {current_month} (seasonal adjustment applied)")
    
    def get_valid_input(self, prompt, input_type=int, min_value=None, max_value=None):
        """Helper function to get validated input"""
        while True:
            try:
                user_input = input(prompt).strip()
                if input_type == float:
                    user_input = user_input.replace(',', '')
                value = input_type(user_input)
                
                if min_value is not None and value < min_value:
                    print(f"Value must be at least {min_value}")
                    continue
                    
                if max_value is not None and value > max_value:
                    print(f"Value must be at most {max_value}")
                    continue
                    
                return value
            except ValueError:
                print(f"Invalid input. Please enter a valid {input_type.__name__}.")
    
    def get_seasonal_discount(self, num_nights):
        """Calculate seasonal discount based on length of stay"""
        discount_array = np.array([0, 0.05, 0.10, 0.15, 0.20])  # Discount tiers
        if num_nights >= 7:
            return 0.20  # 20% off for weekly stays
        elif num_nights >= 5:
            return 0.15  # 15% off for 5+ nights
        elif num_nights >= 3:
            return 0.10  # 10% off for 3+ nights
        else:
            return 0.0
    
    def calculate_bill(self):
        """Main billing calculation function with min-max pricing"""
        print(f"\n{'='*70}")
        print(f"         {self.hotel_name} - ADVANCED BILLING SYSTEM")
        print(f"{'='*70}")
        
        # Display room options with dynamic pricing
        self.display_room_options(show_dynamic=True)
        
        # Get booking details
        print("\n📋 BOOKING DETAILS")
        print("-" * 50)
        
        # Room type selection
        room_choice = self.get_valid_input(
            f"Select room type (1-{len(self.room_types)}): ", 
            int, 1, len(self.room_types)
        ) - 1
        
        room_type = self.room_types[room_choice]
        min_cost = self.min_costs[room_choice]
        max_cost = self.max_costs[room_choice]
        room_category = self.room_categories[room_choice]
        
        # Get dynamic base price
        base_price = self.calculate_dynamic_price(min_cost, max_cost)
        
        # Number of rooms
        num_rooms = self.get_valid_input("Number of rooms to book: ", int, 1, 10)
        
        # Number of nights
        num_nights = self.get_valid_input("Number of nights: ", int, 1, 30)
        
        # Number of people (max 3 per room for standard, 4 for suite)
        max_people = num_rooms * (4 if 'Suite' in room_type else 3)
        num_people = self.get_valid_input(
            f"Total number of people (max {max_people}): ", 
            int, 1, max_people
        )
        
        # Extra bedding
        extra_bedding_input = input("Extra bedding required? (yes/no): ").lower().strip()
        extra_bedding = extra_bedding_input in ['yes', 'y']
        num_extra_beds = 0
        if extra_bedding:
            max_extra_beds = num_rooms * 2
            num_extra_beds = self.get_valid_input(
                f"Number of extra beds (max {max_extra_beds}): ", 
                int, 1, max_extra_beds
            )
        
        # Meals
        print("\n🍽️ MEAL OPTIONS:")
        print("1. Room only (No meals) - ₹0")
        print("2. Breakfast only - ₹500 per person/day")
        print("3. Breakfast + One Meal - ₹900 per person/day")
        print("4. All meals (Full Board) - ₹1,300 per person/day")
        print("5. Premium Dining - ₹1,800 per person/day")
        meal_choice = self.get_valid_input("Select meal option (1-5): ", int, 1, 5)
        
        # Get seasonal discount
        discount_rate = self.get_seasonal_discount(num_nights)
        
        # Initialize numpy array for cost breakdown (8 elements)
        costs = np.zeros(8)
        # Index mapping:
        # 0: Room Cost (Base)
        # 1: Extra Bedding Cost
        # 2: Meal Cost
        # 3: Luxury Tax (if applicable)
        # 4: Subtotal
        # 5: GST Amount
        # 6: Discount Amount
        # 7: Final Total
        
        # Calculate room cost with dynamic pricing
        costs[0] = base_price * num_rooms * num_nights
        
        # Calculate meal costs
        meal_rates = np.array([0, 500, 900, 1300, 1800])
        meal_cost_per_person = meal_rates[meal_choice - 1]
        costs[2] = meal_cost_per_person * num_people * num_nights
        
        # Calculate extra bedding cost (₹1000 per bed per night)
        if extra_bedding:
            costs[1] = 1000 * num_extra_beds * num_nights
        
        # Apply luxury tax for premium categories (10%)
        if room_category in ['Luxury', 'Premium']:
            costs[3] = costs[0] * 0.10
        
        # Calculate subtotal
        costs[4] = np.sum(costs[:4])
        
        # Calculate discount
        costs[6] = costs[4] * discount_rate
        
        # Calculate GST (variable rates based on room category)
        gst_rates = np.array([0.12, 0.18, 0.28])  # Economy: 12%, Premium: 18%, Luxury: 28%
        if room_category == 'Economy':
            gst_rate = gst_rates[0]
        elif room_category == 'Premium':
            gst_rate = gst_rates[1]
        else:  # Luxury
            gst_rate = gst_rates[2]
        
        # GST applied after discount
        taxable_amount = costs[4] - costs[6]
        costs[5] = taxable_amount * gst_rate
        
        # Calculate final total
        costs[7] = taxable_amount + costs[5]
        
        # Generate detailed bill
        self.generate_advanced_bill(
            room_type, room_category, num_rooms, num_nights, num_people,
            extra_bedding, num_extra_beds, meal_choice, costs,
            base_price, discount_rate, gst_rate
        )
        
        return costs[7]
    
    def generate_advanced_bill(self, room_type, room_category, num_rooms, num_nights, 
                              num_people, extra_bedding, num_extra_beds, meal_choice,
                              costs, base_price, discount_rate, gst_rate):
        """Generate and display detailed advanced bill"""
        
        meal_options = ["Room Only", "Breakfast Only", "Breakfast + One Meal", 
                       "All Meals", "Premium Dining"]
        
        print(f"\n{'='*80}")
        print(f"{self.hotel_name:^80}")
        print(f"{'ADVANCED TAX INVOICE':^80}")
        print(f"{'='*80}")
        print(f"Date & Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"Invoice No: INV{np.random.randint(100000, 999999)}")
        print(f"GSTIN: 29{np.random.randint(100000, 999999)}Z{np.random.randint(10, 99)}")
        print(f"{'-'*80}")
        
        # Booking Summary
        print(f"\n📊 BOOKING SUMMARY")
        print(f"{'-'*80}")
        print(f"Room Type: {room_type} ({room_category} Category)")
        print(f"Dynamic Base Price: ₹{base_price:,.2f} per night")
        print(f"Number of Rooms: {num_rooms}")
        print(f"Number of Nights: {num_nights}")
        print(f"Number of Guests: {num_people}")
        print(f"Meal Plan: {meal_options[meal_choice-1]}")
        print(f"Extra Bedding: {'Yes' if extra_bedding else 'No'}", end="")
        if extra_bedding:
            print(f" ({num_extra_beds} beds @ ₹1,000 per bed/night)")
        else:
            print()
        
        # Cost Breakdown
        print(f"\n💰 DETAILED COST BREAKDOWN")
        print(f"{'-'*80}")
        print(f"{'Description':<50} {'Amount (₹)':>25}")
        print(f"{'-'*80}")
        
        # Room charges
        print(f"Room Charges ({room_type})")
        print(f"  Base rate: ₹{base_price:,.2f} × {num_rooms} rooms × {num_nights} nights")
        print(f"{'':<50} {costs[0]:>25,.2f}")
        
        # Extra bedding
        if extra_bedding:
            print(f"\nExtra Bedding Charges")
            print(f"  {num_extra_beds} beds × {num_nights} nights @ ₹1,000 per night")
            print(f"{'':<50} {costs[1]:>25,.2f}")
        
        # Meal charges
        if costs[2] > 0:
            meal_rate = costs[2] / (num_people * num_nights)
            print(f"\nMeal Charges ({meal_options[meal_choice-1]})")
            print(f"  ₹{meal_rate:.0f} × {num_people} persons × {num_nights} nights")
            print(f"{'':<50} {costs[2]:>25,.2f}")
        
        # Luxury tax for premium rooms
        if costs[3] > 0:
            print(f"\nLuxury Tax (10% on room charges)")
            print(f"{'':<50} {costs[3]:>25,.2f}")
        
        print(f"{'-'*80}")
        print(f"{'SUBTOTAL':<50} {costs[4]:>25,.2f}")
        
        # Discount if applicable
        if costs[6] > 0:
            print(f"\n🎁 DISCOUNTS APPLIED")
            print(f"Long Stay Discount ({discount_rate*100:.0f}% for {num_nights} nights)")
            print(f"{'':<50} -{costs[6]:>24,.2f}")
            print(f"{'Amount after discount':<50} {(costs[4]-costs[6]):>25,.2f}")
        
        # Tax Details
        print(f"\n🧾 TAX CALCULATION")
        print(f"{'-'*80}")
        print(f"Taxable Amount: ₹{costs[4]-costs[6]:,.2f}")
        print(f"GST Rate Applied: {gst_rate*100:.0f}% ({room_category} Category)")
        print(f"GST Amount: ₹{costs[5]:,.2f}")
        
        print(f"\n{'='*80}")
        print(f"{'GRAND TOTAL':<50} ₹{costs[7]:>25,.2f}")
        print(f"{'='*80}")
        
        # Payment Summary with EMI option
        print(f"\n💳 PAYMENT SUMMARY")
        print(f"{'-'*80}")
        
        # Per person/room/night costs using numpy
        per_person_cost = costs[7] / num_people
        per_room_cost = costs[7] / num_rooms
        per_night_cost = costs[7] / num_nights
        
        print(f"Cost per person: ₹{per_person_cost:,.2f}")
        print(f"Cost per room: ₹{per_room_cost:,.2f}")
        print(f"Cost per night: ₹{per_night_cost:,.2f}")
        
        # EMI Options (if amount > 5000)
        if costs[7] > 5000:
            print(f"\n💱 EMI OPTIONS AVAILABLE:")
            emi_3months = costs[7] / 3
            emi_6months = costs[7] / 6
            emi_12months = costs[7] / 12
            print(f"  3 Months EMI: ₹{emi_3months:,.2f}/month")
            print(f"  6 Months EMI: ₹{emi_6months:,.2f}/month")
            print(f"  12 Months EMI: ₹{emi_12months:,.2f}/month")
        
        print(f"\n{'='*80}")
        print(f"Thank you for choosing {self.hotel_name}!")
        print(f"We hope you have a pleasant stay! 🌟")
        print(f"{'='*80}\n")
    
    def compare_room_prices(self):
        """Compare min and max prices across room types using numpy"""
        print(f"\n{'='*70}")
        print(f"         {self.hotel_name} - PRICE COMPARISON")
        print(f"{'='*70}")
        
        # Price range analysis
        price_ranges = self.max_costs - self.min_costs
        avg_min = np.mean(self.min_costs)
        avg_max = np.mean(self.max_costs)
        
        print(f"\n📊 PRICE RANGE ANALYSIS:")
        print("-" * 50)
        print(f"Average Minimum Price: ₹{avg_min:,.2f}")
        print(f"Average Maximum Price: ₹{avg_max:,.2f}")
        print(f"Average Price Variation: ₹{np.mean(price_ranges):,.2f}")
        print(f"Maximum Price Variation: ₹{np.max(price_ranges):,.2f}")
        
        # Category-wise analysis
        print(f"\n📈 CATEGORY-WISE ANALYSIS:")
        print("-" * 50)
        
        for category in np.unique(self.room_categories):
            mask = self.room_categories == category
            cat_min = np.mean(self.min_costs[mask])
            cat_max = np.mean(self.max_costs[mask])
            cat_rooms = np.sum(mask)
            
            print(f"\n{category} Category:")
            print(f"  Number of Room Types: {cat_rooms}")
            print(f"  Average Min Price: ₹{cat_min:,.2f}")
            print(f"  Average Max Price: ₹{cat_max:,.2f}")
            print(f"  Price Range: ₹{cat_max - cat_min:,.2f}")
        
        # Best value recommendations
        print(f"\n💡 BEST VALUE RECOMMENDATIONS:")
        print("-" * 50)
        
        # Calculate value score (lower price range = better value)
        value_scores = 1 / (price_ranges / self.min_costs)
        best_value_idx = np.argmax(value_scores)
        
        print(f"Best Value Room: {self.room_types[best_value_idx]}")
        print(f"  Price Range: ₹{self.min_costs[best_value_idx]:,.0f} - ₹{self.max_costs[best_value_idx]:,.0f}")
        print(f"  Variation: {(price_ranges[best_value_idx]/self.min_costs[best_value_idx]*100):.1f}%")
    
    def batch_booking_analysis(self):
        """Analyze multiple bookings using numpy arrays"""
        print(f"\n{'='*70}")
        print(f"         {self.hotel_name} - BATCH BOOKING ANALYSIS")
        print(f"{'='*70}")
        
        num_bookings = self.get_valid_input("Enter number of bookings to analyze: ", int, 1, 20)
        
        # Arrays to store booking data
        booking_room_indices = np.zeros(num_bookings, dtype=int)
        booking_nights = np.zeros(num_bookings)
        booking_people = np.zeros(num_bookings)
        booking_costs = np.zeros(num_bookings)
        
        print("\n📋 Enter quick details for each booking:")
        print("-" * 50)
        
        for i in range(num_bookings):
            print(f"\nBooking #{i+1}:")
            self.display_room_options(show_dynamic=False)
            room_choice = self.get_valid_input(
                f"Select room type (1-{len(self.room_types)}): ",
                int, 1, len(self.room_types)
            ) - 1
            
            booking_room_indices[i] = room_choice
            booking_nights[i] = self.get_valid_input("Number of nights: ", int, 1, 30)
            booking_people[i] = self.get_valid_input("Number of people: ", int, 1, 10)
            
            # Quick cost estimation (using average price)
            avg_price = (self.min_costs[room_choice] + self.max_costs[room_choice]) / 2
            booking_costs[i] = avg_price * booking_nights[i]
        
        # Statistical analysis using numpy
        print(f"\n{'='*70}")
        print("BATCH BOOKING ANALYTICS:")
        print(f"{'='*70}")
        
        print(f"\n📊 OVERALL STATISTICS:")
        print("-" * 50)
        print(f"Total Bookings Analyzed: {num_bookings}")
        print(f"Total Estimated Revenue: ₹{np.sum(booking_costs):,.2f}")
        print(f"Average Booking Value: ₹{np.mean(booking_costs):,.2f}")
        print(f"Median Booking Value: ₹{np.median(booking_costs):,.2f}")
        
        if num_bookings > 1:
            print(f"Standard Deviation: ₹{np.std(booking_costs):,.2f}")
            print(f"25th Percentile: ₹{np.percentile(booking_costs, 25):,.2f}")
            print(f"75th Percentile: ₹{np.percentile(booking_costs, 75):,.2f}")
        
        print(f"\n👥 GUEST STATISTICS:")
        print("-" * 50)
        print(f"Total Guests: {int(np.sum(booking_people))}")
        print(f"Average Guests per Booking: {np.mean(booking_people):.1f}")
        print(f"Total Room Nights: {int(np.sum(booking_nights))}")
        print(f"Average Stay Duration: {np.mean(booking_nights):.1f} nights")
        
        # Room type distribution with percentages
        print(f"\n🏨 ROOM TYPE DISTRIBUTION:")
        print("-" * 50)
        unique_indices, counts = np.unique(booking_room_indices, return_counts=True)
        
        for idx, count in zip(unique_indices, counts):
            percentage = (count / num_bookings) * 100
            print(f"{self.room_types[idx]:<25} {count:>3} booking(s) ({percentage:>5.1f}%)")
        
        # Revenue by category
        print(f"\n💰 REVENUE BY CATEGORY:")
        print("-" * 50)
        
        for category in np.unique(self.room_categories):
            category_mask = np.isin(booking_room_indices, 
                                   np.where(self.room_categories == category)[0])
            if np.any(category_mask):
                cat_revenue = np.sum(booking_costs[category_mask])
                cat_bookings = np.sum(category_mask)
                print(f"{category:<15} {cat_bookings:>3} bookings - ₹{cat_revenue:>12,.2f}")
    
    def main_menu(self):
        """Main menu for finance system"""
        while True:
            print(f"\n{'='*70}")
            print(f"   {self.hotel_name} - FINANCE MANAGEMENT SYSTEM")
            print(f"{'='*70}")
            print("1. Calculate Individual Booking Bill (with Dynamic Pricing)")
            print("2. Batch Booking Analysis")
            print("3. Compare Room Prices & Categories")
            print("4. View All Room Types & Pricing")
            print("5. Exit")
            print(f"{'='*70}")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                try:
                    self.calculate_bill()
                except Exception as e:
                    print(f"\nError calculating bill: {e}")
            elif choice == '2':
                try:
                    self.batch_booking_analysis()
                except Exception as e:
                    print(f"\nError in batch analysis: {e}")
            elif choice == '3':
                self.compare_room_prices()
            elif choice == '4':
                self.display_room_options(show_dynamic=True)
            elif choice == '5':
                print(f"\n{'='*70}")
                print(f"Thank you for using {self.hotel_name} Finance System!")
                print("Have a wonderful day! 🌟")
                print(f"{'='*70}\n")
                break
            else:
                print("Invalid choice! Please try again.")

def create_sample_rooms_file():
    """Create a sample rooms_min_max.csv file"""
    sample_data = [
        ['Room Type', 'Min Price (₹)', 'Max Price (₹)', 'Category'],
        ['Standard Single', 2000, 3500, 'Economy'],
        ['Standard Double', 3000, 4500, 'Economy'],
        ['Deluxe Single', 4000, 6000, 'Premium'],
        ['Deluxe Double', 5000, 7000, 'Premium'],
        ['Suite', 8000, 12000, 'Luxury'],
        ['Premium Suite', 11000, 15000, 'Luxury'],
        ['Family Room', 6000, 9000, 'Premium'],
        ['Executive Room', 7000, 10000, 'Premium'],
        ['Presidential Suite', 15000, 25000, 'Luxury'],
        ['Garden View Room', 3500, 5500, 'Economy'],
        ['Ocean View Room', 4500, 6500, 'Premium'],
        ['Honeymoon Suite', 13000, 18000, 'Luxury']
    ]
    
    with open('rooms_min_max.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)
    
    print("✓ Sample rooms_min_max.csv created successfully!")

if __name__ == "__main__":
    try:
        # Check if rooms_min_max.csv exists
        if not os.path.exists('rooms_min_max.csv'):
            print("rooms_min_max.csv not found. Creating sample file...")
            create_sample_rooms_file()
            print()
        
        # Initialize and run the finance system
        finance_system = HotelFinanceSystem()
        finance_system.main_menu()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check your rooms_min_max.csv file format.")