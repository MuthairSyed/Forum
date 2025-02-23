from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def format_data(data):
    """
    Formats the input data by removing extra spaces and preparing it for output.
    """
    formatted_data = {}
    for line in data:
        line = line.strip()  # Remove leading/trailing spaces
        # Remove all extra spaces between words (normalize spaces)
        line = " ".join(line.split())
        
        # Find the last space and treat the part after it as the forum count
        if " " in line:
            *name_parts, count = line.rsplit(" ", 1)
            name = " ".join(name_parts).strip()
            count = count.strip()
            
            # Check if the count is a valid number
            if count.isdigit():
                formatted_data[name] = count
            else:
                print(f"Invalid forum count detected (not a number): {line}")
        else:
            print(f"Invalid input format (missing count): {line}")
    
    return formatted_data

def generate_report(data):
    """
    Generates and returns the formatted report based on the input data.
    """
    # Sort the data based on forum counts (high to low)
    sorted_data = sorted(data.items(), key=lambda x: int(x[1]), reverse=True)
    
    # Calculate the total number of forums done this week
    total_forums = sum(int(count) for count in data.values())
    # Calculate the average number of forums done
    average_forums = total_forums / len(data) if len(data) > 0 else 0
    
    report = []
    report.append("Hello <@&1034522315230302238> Forum counts for this week!! If you spot any mistakes, DM me with the proofs and I'll look into it.\n")
    report.append("```js")
    
    # Display each name : count with underlines
    for name, count in sorted_data:
        report.append(f"{name}: {count}")
        report.append(f"{'-' * (len(name) + 1)}")  # Underline only the name part
    
    report.append("```")
    
    # Display the leaderboard
    if len(sorted_data) > 0:
        report.append(f"🥇 {sorted_data[0][0]}: {sorted_data[0][1]}")
    if len(sorted_data) > 1:
        report.append(f"🥈 {sorted_data[1][0]}: {sorted_data[1][1]}")
    if len(sorted_data) > 2:
        report.append(f"🥉 {sorted_data[2][0]}: {sorted_data[2][1]}")
    
    # Average and Total after names
    report.append(f"```py\nAverage: {average_forums:.2f}")
    report.append(f"Total Forums Done this week: {total_forums}\n```")
    
    # Friendly reminders
    report.append("\n**Friendly Reminders:**")
    report.append("- Put \"Reviewing\" on only 1 forum at a time and review it promptly; **__do not claim multiple at once__**")
    report.append("- Take oldest forums first, even if (New)er ones are Incorrect Format/Title:")    
    report.append("> https://discord.com/channels/936323011664031795/1034533918348689548/1160931017406808144")
    report.append("> (*See here and Bookmark to quickly access oldest Pending forums *https://discord.com/channels/936323011664031795/1034524537158631535/1149747608949112947)")
    report.append("Feel free to DM me for your forum account, to report errors with proof, or for anything forum-related. We're a team here to help each other succeed. If you face challenges, collaborate with other admins or check the Admin Discord for guidance. Great work, everyone!")

    return "\n".join(report)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_report', methods=['POST'])
def generate_report_route():
    data = request.json.get('data', [])
    formatted_data = format_data(data)
    
    if formatted_data:
        report = generate_report(formatted_data)
        return jsonify({"report": report})
    else:
        return jsonify({"error": "No valid data entered."})

if __name__ == "__main__":
    app.run(debug=True)
