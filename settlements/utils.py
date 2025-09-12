

import heapq
from decimal import Decimal, ROUND_HALF_UP
from expenses.models import Expense
from expenseparticipant.models import ExpenseParticipant
from settlements.models import Settlement
from user.models import User

def calculate_settlements_for_group(group):
    balances = {}

    # Calculate balances per user
    for expense in Expense.objects.filter(group_id=group.id):
        participants = ExpenseParticipant.objects.filter(expense=expense)
        num_participants = participants.count()
        if num_participants == 0:
            continue

        # Equal split amount per participant
        equal_share = (expense.amount / num_participants).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        for p in participants:
            user_key = p.user.username  # or p.user.email
            balances.setdefault(user_key, Decimal('0.00'))

            # Amount paid minus share
            # If user paid more than share → positive (they are owed)
            # If user paid less than share → negative (they owe)
            balances[user_key] += (p.paid_amount - equal_share)

    print("Balances:", balances)

    if not balances:
        return []

    # Prepare heaps for creditors and debtors
    min_heap = []  # debtors (negative balances)
    max_heap = []  # creditors (positive balances)
    counter = 0

    for user, balance in balances.items():
        balance = balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if balance > 0:
            heapq.heappush(max_heap, (-balance, counter, user))  # negative for max heap
        elif balance < 0:
            heapq.heappush(min_heap, (balance, counter, user))   # already negative
        counter += 1

    # 3️ Calculate settlements
    settlements = []

    while min_heap and max_heap:
        debt_amount, _, debtor = heapq.heappop(min_heap)   # negative
        credit_amount, _, creditor = heapq.heappop(max_heap)  # negative

        debt_amount_abs = -debt_amount
        credit_amount_abs = -credit_amount

        transfer_amount = min(debt_amount_abs, credit_amount_abs).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Save settlement to DB
        Settlement.objects.update_or_create(
            group=group,
            lender=User.objects.get(username=creditor),
            borrower=User.objects.get(username=debtor),
            defaults={'amount': transfer_amount}
        )

        settlements.append({
            "from_user": debtor,
            "to_user": creditor,
            "amount": float(transfer_amount)
        })

        # Update remaining amounts
        remaining_debt = debt_amount_abs - transfer_amount
        remaining_credit = credit_amount_abs - transfer_amount

        if remaining_debt > 0:
            heapq.heappush(min_heap, (-remaining_debt, counter, debtor))  # keep negative
            counter += 1
        if remaining_credit > 0:
            heapq.heappush(max_heap, (-remaining_credit, counter, creditor))
            counter += 1

    print("Final Settlements:", settlements)
    return settlements
