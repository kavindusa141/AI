import sys, os
# Ensure Python finds the agent/ folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, session, send_file
from agent.agent import TourPlanningAgent

# PDF generation imports
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Import NLP module (optional)
try:
    from agent.nlp_utils import extract_interests_from_text
    HAS_NLP = True
except ImportError:
    HAS_NLP = False

app = Flask(__name__)
app.secret_key = "wanderlust-ai-secret-key"  # required for session

# Initialize Agent
agent = TourPlanningAgent("../data/tour_packages.json")



@app.route("/", methods=["GET", "POST"])
def index():
    plan = None
    map_markers = []

    if request.method == "POST":
        try:
            # 1. Get Inputs
            budget = float(request.form["budget"])
            days = int(request.form["days"])

            # 2. NLP Processing
            if HAS_NLP:
                raw_text = request.form["interests"]
                interests = extract_interests_from_text(raw_text)
            else:
                interests = [i.strip() for i in request.form["interests"].split(",")]

            # 3. Travel Style
            travel_style = request.form.get("travel_style", "default")

            goals = {
                "budget": budget,
                "days": days,
                "interests": interests,
                "travel_style": travel_style
            }

            # 4. Run AI Agent
            packages, activities, itinerary_data, explanation = agent.run(goals)

            if packages:
                # 5. Build plan object
                plan = {
                    "summary": packages,
                    "days": days,
                    "daily_activities": itinerary_data["daily_activities"],
                    "explanation": explanation
                }

                # 🔑 Store plan for PDF download
                session["plan"] = plan

                # 6. Extract map markers
                for day in itinerary_data["daily_activities"]:
                    for act in day:
                        if "lat" in act and "lon" in act:
                            map_markers.append({
                                "lat": act["lat"],
                                "lon": act["lon"],
                                "name": act["name"]
                            })

        except Exception as e:
            print(f"❌ Error: {e}")

    return render_template("index.html", plan=plan, map_markers=map_markers)


# 📄 PDF DOWNLOAD ROUTE
@app.route("/download-plan")
def download_plan():

    plan = session.get("plan")
    if not plan:
        return "No tour plan available", 400

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(40, y, "Wanderlust AI - Tour Plan")
    y -= 30

    # Summary
    pdf.setFont("Helvetica", 12)
    pdf.drawString(40, y, f"Duration: {plan['days']} Days")
    y -= 20
    pdf.drawString(40, y, f"Total Cost: ${plan['explanation']['total_cost']}")
    y -= 30

    # Daily Itinerary
    for i, day in enumerate(plan["daily_activities"], start=1):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, y, f"Day {i}")
        y -= 20

        pdf.setFont("Helvetica", 11)
        for act in day:
            pdf.drawString(60, y, f"- {act['name']} (${act['cost']})")
            y -= 15

            if y < 60:
                pdf.showPage()
                y = height - 40

        y -= 10

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="wanderlust_ai_tour_plan.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
