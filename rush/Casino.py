#!/usr/bin/env python3

import random

# ข้อมูลหลัก
players = {}  # {"ชื่อ": {"balance": 100, "wins": 0, "losses": 0}}
history = []  # [{"player": "ชื่อ", "game": "Dice", "bet": 100, "result": "win"}]
START_MONEY = 100  # เงินเริ่มต้นของผู้เล่นใหม่ทุกคน


# --- จำนวนเงินเติมเงินและเงินเดิมพันจากผู้ใช้ (คืนค่า None ถ้าไม่ใช่ตัวเลข) ---
def read_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("❌ ใส่เป็นตัวเลขจำนวนเงินเท่านั้น!")
        return None


# --- ตรวจสอบผู้เล่น ---
def player_exists(player_name):
    if player_name not in players:
        print("❌ ไม่พบผู้เล่นนี้!")
        return False
    return True


# --- แสดงรายชื่อผู้เล่น แล้วให้เลือก (คืนชื่อที่เลือก หรือ None ถ้าไม่มีผู้เล่น/ไม่พบชื่อ) ---
def choose_player(prompt="ชื่อผู้เล่น: "):
    if not players:
        print("❌ ยังไม่มีผู้เล่น! สร้างผู้เล่นก่อน")
        return None
    print("👥 ผู้เล่น:", ", ".join(players.keys()))
    name = input(prompt).strip()
    if not player_exists(name):
        return None
    return name


# --- ตรวจสอบเงินเดิมพัน ---
def check_bet(player_name, bet):
    if not player_exists(player_name):
        return False
    if bet <= 0:
        print("❌ เงินเดิมพันต้องมากกว่า 0")
        return False
    if bet > players[player_name]["balance"]:
        print(f"❌ เงินไม่พอ! มีแค่ {players[player_name]['balance']} บาท")
        return False
    return True


# --- อัปเดตผลการเล่น ---
def update_result(player_name, game, bet, result):
    p = players[player_name]
    if result == "win":
        p["balance"] += bet
        p["wins"] += 1
        print(f"🎉 ชนะ! +{bet} บาท | คงเหลือ: {p['balance']} บาท")
    elif result == "loss":
        p["balance"] -= bet
        p["losses"] += 1
        print(f"😢 แพ้! -{bet} บาท | คงเหลือ: {p['balance']} บาท")
    else:
        print(f"🤝 เสมอ! คงเหลือ: {p['balance']} บาท")
    history.append({"player": player_name, "game": game, "bet": bet, "result": result})


# --- สร้างผู้เล่นใหม่ (ได้เงินเริ่มต้นอัตโนมัติ) ---
def create_player(name):
    if name in players:
        print("❌ ชื่อนี้มีอยู่แล้ว!")
        return
    players[name] = {"balance": START_MONEY, "wins": 0, "losses": 0}
    print(f"✅ สร้างผู้เล่น '{name}' สำเร็จ! | เงินเริ่มต้น: {START_MONEY} บาท")


# --- เติมเงิน ---
def deposit(player_name, amount):
    if not player_exists(player_name):
        return
    if amount <= 0:
        print("❌ จำนวนเงินต้องมากกว่า 0")
        return
    players[player_name]["balance"] += amount
    print(f"✅ เติมเงินสำเร็จ! คงเหลือ: {players[player_name]['balance']} บาท")


# --- ลบผู้เล่น (พร้อมประวัติ) ---
def delete_player(player_name):
    if not player_exists(player_name):
        return
    del players[player_name]
    history[:] = [r for r in history if r["player"] != player_name]
    print(f"🗑️ ลบผู้เล่น '{player_name}' แล้ว")


# --- เกม Dice (เปิดลูกแรกให้ดู → ทาย → เปิดลูกที่สอง) ---
def play_dice(player_name, bet):
    if not check_bet(player_name, bet):
        return

    # ทอยครั้งเดียว แล้วใช้ค่าเดิมตลอดทั้งเกม
    dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
    total = dice1 + dice2
    print(f"\n🎲 ลูกที่ 1: {dice1} | ลูกที่ 2: ? \nรวม: ?")
    print("LOW = 1-7 | HIGH = 8-12")
    while True:
        guess = input("ทาย LOW | HIGH: ").strip().upper()
        if guess in ["LOW", "HIGH"]:
            break
        print("❌ พิมพ์ LOW หรือ HIGH เท่านั้น!")
    print(f"\n🎲! ลูกที่ 1: {dice1} | ลูกที่ 2: {dice2} \nรวม: {total}")

      # LOW = รวม 7 ลงมา | HIGH = รวม 8 ขึ้นไป
    if total <= 7:
        actual = "LOW"
    else:
        actual = "HIGH"
    print(f"ผลที่ได้: {actual}")
 
    win = guess == actual
    update_result(player_name, "Dice", bet, "win" if win else "loss")

# --- ดูประวัติ ---
def show_history(player_name):
    if not player_exists(player_name):
        return
    records = [r for r in history if r["player"] == player_name]
    if not records:
        print("ยังไม่มีประวัติการเล่น")
        return
    print(f"\n📜 ประวัติของ '{player_name}':")
    for i, r in enumerate(records, 1):
        print(f" {i}. {r['game']} | เดิมพัน: {r['bet']} | ผล: {r['result']}")

# --- ดู Leaderboard ---
def show_leaderboard():
    if not players:
        print("❌ ยังไม่มีผู้เล่น!")
        return
    print("\n🏆 LEADERBOARD:")
    sorted_p = sorted(players.items(), key=lambda x: x[1]["balance"], reverse=True)
    for i, (name, d) in enumerate(sorted_p, 1):
        total = d["wins"] + d["losses"]
        rate = round(d["wins"] / total * 100) if total > 0 else 0
        print(f" {i}. {name} | เงิน: {d['balance']} บาท | W:{d['wins']} L:{d['losses']} | Win Rate: {rate}%")

# --- เมนูหลัก ---
def main():
    print("=============================")
    print("🎰 ยินดีต้อนรับสู่ CASINO 🎰")
    print("=============================")

    while True:
        print("\n1. สร้างผู้เล่นใหม่")
        print("2. เล่น Dice")
        print("3. ดูประวัติ")
        print("4. ดู Leaderboard")
        print("5. เติมเงิน")
        print("6. ลบผู้เล่น")
        print("7. ออก")
        choice = input("\nเลือก (1-7): ").strip()

        if choice == "1":
            name = input("ชื่อผู้เล่น: ").strip()
            if not name:
                print("❌ ชื่อห้ามว่าง!")
                continue
            create_player(name)

        elif choice == "2":
            name = choose_player()
            if name is None:
                continue
            bet = read_int("เงินเดิมพัน: ")
            if bet is None:
                continue
            play_dice(name, bet)

        elif choice == "3":
            name = choose_player()
            if name is None:
                continue
            show_history(name)

        elif choice == "4":
            show_leaderboard()
        
        elif choice == "5":
            name = choose_player()
            if name is None:
                continue
            amount = read_int("จำนวนเงินที่เติม: ")
            if amount is None:
                continue
            deposit(name, amount)

        elif choice == "6":
            name = choose_player("ชื่อผู้เล่นที่ต้องการลบ: ")
            if name is None:
                continue
            delete_player(name)

        elif choice == "7":
            print("\n👋 ขอบคุณที่มาเล่น! แล้วพบกันใหม่ 🎰")
            break

        else:
            print("❌ ไม่มีเมนูนี้! เลือก 1-7")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 ออกจากโปรแกรม")
