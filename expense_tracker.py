import datetime
import json
import os
import matplotlib.pyplot as plt
DATA_FILE="expenses.json"
#load expenses from file if exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE,"r") as file:
        expenses=json.load(file)
else:
    expenses=[]

def visualize_expenses():
    if not expenses:
        print("no expenses to visualize yet")
        return
    summary={}
    for exp in expenses:
        category=exp['category']
        summary[category]=summary.get(category,0)+exp['amount']
    categories=list(summary.keys())
    amounts=list(summary.values())
    plt.figure(figsize=(7,7))
    plt.pie(amounts,labels=categories,autopct="%1.1f%%",startangle=140)
    plt.title("spending by category")
    plt.show()

#Function to save expenses to file
def save_expenses():
    with open(DATA_FILE ,"w") as file:
        json.dump(expenses,file,indent=4)#python object -> json file
#Add new expense
def add_expense():
    date=datetime.date.today().strftime("%Y-%m-%d")
    category=input("enter category (food/Travel/Rent/other):")
    try:
        amount=float(input("enter amount: "))
    except ValueError:
        print("❌ Invalid amount!")
        return
    expense={"date":date,
             "category":category,
             "amount":amount}
    expenses.append(expense)
    save_expenses()
    print("✅ Expense added!")


def view_expenses():
        if not expenses:
            print("No expenses recorded yet")
        else:
            print("\n📄 All Expenses:")
            for i,exp in enumerate(expenses,start=1):
                print(f"{i}.{exp['date']}-{exp['category']}-₹{exp['amount']}")




def total_spent():
    total=sum(exp['amount'] for exp in expenses)
    print(f"💰 Total spent:₹ {total}")


def category_summary():
    if not expenses:
        print("no expenses recorded yet")
        return
    summary={}
    for exp in expenses:
        category=exp['category']
        summary[category]=summary.get(category,0)+exp['amount']
    print("\n📊 Spending by Category:")
    for cat,amt in summary.items():
        print(f"{cat}:{amt}")

def main():
    while True:
        print("\n=====expense Tracker===")
        print("1.Add expense")
        print("2.View expenses")
        print("3.View Total spent")
        print("4.category-wise Summary")
        print("5.visualize expenses")
        print("6.exit")
        choice=int(input("choose an option: "))
        if choice ==1:
            add_expense()
        elif choice==2:
            view_expenses()
        elif choice==3:
            total_spent()
        elif choice==4:
            category_summary()
        elif choice==5:
            visualize_expenses()
        elif choice=="6":
            print("good bye!")
            break
        else:
            print("❌ Invalid choice! Try again.") 
if __name__=="__main__":
    main()