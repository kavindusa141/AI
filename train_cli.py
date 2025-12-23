import os
import sys
import time

# Ensure Python finds your modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.agent import TourPlanningAgent

# Try to import NLP, fallback if missing
try:
    from agent.nlp_utils import extract_interests_from_text
    HAS_NLP = True
except ImportError:
    HAS_NLP = False

# ==========================================
# 🎨 TERMINAL COLORS
# ==========================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colors.HEADER + Colors.BOLD + """
    ========================================
       🌍 AI TOUR AGENT - TRAINING HUB 🚀
    ========================================
    """ + Colors.END)

def main():
    print(Colors.CYAN + "⚙️  Initializing AI Brain..." + Colors.END)
    try:
        agent = TourPlanningAgent("data/tour_packages.json")
    except Exception as e:
        print(Colors.RED + f"❌ Critical Error: {e}" + Colors.END)
        return

    while True:
        print_banner()
        
        # ==========================================
        # 1️⃣ INTERACTIVE INPUT
        # ==========================================
        try:
            print(Colors.YELLOW + "📋 TRIP PARAMETERS" + Colors.END)
            try:
                budget = int(input(f"   💰 Enter Budget ({Colors.GREEN}USD{Colors.END}): "))
                days = int(input(f"   📅 Enter Duration ({Colors.GREEN}Days{Colors.END}): "))
            except ValueError:
                print(Colors.RED + "   ⚠️ Please enter valid numbers." + Colors.END)
                time.sleep(1)
                continue
            
            print(f"\n{Colors.YELLOW}🎭 TRAVEL PREFERENCES{Colors.END}")
            print(f"   Styles: [default, solo, family, luxury]")
            style = input("   👤 Select Style: ").lower().strip()
            if style not in ['solo', 'family', 'luxury']:
                style = 'default'

            if HAS_NLP:
                raw_interest = input(f"\n   💭 Describe your dream trip ({Colors.CYAN}Natural Language{Colors.END}):\n   > ")
                interests = extract_interests_from_text(raw_interest)
                print(f"   ✨ AI Detected: {Colors.CYAN}{', '.join(interests)}{Colors.END}")
            else:
                raw_interest = input("   ❤️ Enter Interests (comma separated): ")
                interests = [i.strip() for i in raw_interest.split(",") if i.strip()]

            goals = {
                "budget": budget,
                "days": days,
                "interests": interests,
                "travel_style": style
            }

            # ==========================================
            # 2️⃣ RUNNING AGENT
            # ==========================================
            print(f"\n{Colors.BLUE}🧠 AI is thinking...{Colors.END}")
            time.sleep(0.5) 
            
            packages, activities, itinerary_data, explanation = agent.run(goals)

            if packages is None:
                print(Colors.RED + "\n❌ No feasible plan found. Try increasing budget or changing interests." + Colors.END)
                input("\nPress Enter to try again...")
                continue

            # ==========================================
            # 3️⃣ DISPLAY RESULTS
            # ==========================================
            print("\n" + "="*50)
            print(Colors.GREEN + Colors.BOLD + "🌍 GENERATED TOUR PACKAGE" + Colors.END)
            print("="*50)

            dest_list = set(d for p in packages for d in p["destinations"])
            print(f"{Colors.BOLD}📍 Destinations:{Colors.END} {', '.join(dest_list)}")
            print(f"{Colors.BOLD}💵 Total Cost:{Colors.END}   ${explanation['total_cost']}")
            print(f"{Colors.BOLD}⏱️  Duration:{Colors.END}     {goals['days']} Days")

            # Daily Itinerary
            print(f"\n{Colors.YELLOW}🗓️  DAILY ITINERARY{Colors.END}")
            
            # Handle Dictionary Itinerary Format
            if isinstance(itinerary_data, dict) and 'daily_activities' in itinerary_data:
                daily_sched = itinerary_data['daily_activities']
            else:
                daily_sched = [] 

            for i, day_acts in enumerate(daily_sched, 1):
                day_total = sum(a.get('cost', 0) for a in day_acts)
                print(f"\n   {Colors.BOLD}Day {i}{Colors.END} (Est. ${day_total})")
                print(f"   {'='*20}")
                
                if not day_acts or (len(day_acts) == 1 and day_acts[0]['name'] == 'Free Day / Relax'):
                     print(f"     💤 Free Day / Relax")
                else:
                    for a in day_acts:
                        time_icon = "🌅" if a.get('preferred_time') == 'morning' else "🌇" if a.get('preferred_time') == 'evening' else "☀️"
                        print(f"     {time_icon} {a['name']} ({a.get('duration_hours', 0)}h) - {Colors.GREEN}${a.get('cost',0)}{Colors.END}")

            # AI Explanation
            print(f"\n{Colors.CYAN}🤖 AI REASONING{Colors.END}")
            for reason in explanation['reasons']:
                print(f"   • {reason}")
            
            ml_score_disp = explanation.get('ml_score') if explanation.get('ml_score') is not None else "N/A"
            print(f"\n   📊 Rule Score: {explanation['rule_score']} | ML Score: {ml_score_disp}")

            # ==========================================
            # 4️⃣ FEEDBACK LOOP
            # ==========================================
            print("\n" + "-"*50)
            while True:
                try:
                    rating_input = input(f"{Colors.YELLOW}⭐ Rate this plan (1-5): {Colors.END}")
                    rating = int(rating_input)
                    if 1 <= rating <= 5:
                        break
                except ValueError:
                    pass
                print(Colors.RED + "   ⚠️ Invalid. Please enter 1-5." + Colors.END)

            agent.learn(packages, activities, goals, rating)
            print(Colors.GREEN + "✅ Feedback saved! Brain updated." + Colors.END)
            
            if input(f"\n🔄 Train again? (y/n): ").lower() != 'y':
                print(Colors.CYAN + "👋 Goodbye!" + Colors.END)
                break

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(Colors.RED + f"\n⚠️ An unexpected error occurred: {e}" + Colors.END)
            import traceback
            traceback.print_exc()
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()