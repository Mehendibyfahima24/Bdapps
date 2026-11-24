import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# SSC ও HSC শিক্ষার্থীদের জন্য ছোট ও কাজের টিপস
STUDY_TIPS = {
    "ssc": [
        "SSC Tip: কঠিন অধ্যায়ের সূত্র বা সংজ্ঞা পড়ে না দেখে খাতায় ৩ বার লিখুন।",
        "SSC Tip: প্রতি ১ ঘণ্টা পড়ার পর ১০ মিনিট ফোন দূরে রেখে চোখ বিশ্রাম দিন।"
    ],
    "hsc": [
        "HSC Tip: বড় টপিক মুখস্থ না করে মূল পয়েন্ট বা ফ্লোচার্ট বানিয়ে রিভিশন দিন।",
        "HSC Tip: বিগত বোর্ড প্রশ্নের প্যাটার্ন বুঝে সময় ধরে প্র্যাকটিস করুন।"
    ],
    "focus": [
        "Focus Tip: পড়ার সময় নোটিফিকেশন অফ রাখুন এবং সামনে শুধু একটি বিষয়ের বই রাখুন।"
    ]
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "service": "ExamBoostPro - SSC & HSC Study Booster"
    }), 200

@app.route("/ussd", methods=["POST"])
def ussd_webhook():
    """
    bdapps থেকে আসা JSON/Form পেলোড রিসিভ করে পরবর্তী মেনু বা টিপস রিটার্ন করে।
    (লাইভ bdapps পেলোডের ফিল্ড অনুযায়ী প্রয়োজনে নিচের key গুলো মিলিয়ে নিতে হবে।)
    """
    data = request.get_json(silent=True) or request.form.to_dict() or {}

    address = data.get("address", "")
    session_id = data.get("sessionId", "")
    message = str(data.get("message", "")).strip()

    # প্রথমবার মেনু ওপেন করলে বা খালি ইনপুট এলে মূল মেনু দেখান
    if message == "" or message.lower() in ["menu", "start", "0"]:
        reply_text = (
            "ExamBoostPro (SSC & HSC)\n"
            "1. SSC Study Booster\n"
            "2. HSC Study Booster\n"
            "3. Focus & Exam Tip\n"
            "9. Exit"
        )
        return jsonify({
            "sessionId": session_id,
            "address": address,
            "message": reply_text,
            "ussdOperation": "mt-cont"
        }), 200

    if message == "1":
        reply_text = STUDY_TIPS["ssc"][0] + "\n\n0. Main Menu | 9. Exit"
        operation = "mt-cont"
    elif message == "2":
        reply_text = STUDY_TIPS["hsc"][0] + "\n\n0. Main Menu | 9. Exit"
        operation = "mt-cont"
    elif message == "3":
        reply_text = STUDY_TIPS["focus"][0] + "\n\n0. Main Menu | 9. Exit"
        operation = "mt-cont"
    elif message == "9":
        reply_text = "শুভকামনা! মনোযোগ দিয়ে পড়ুন।"
        operation = "mt-fin"
    else:
        reply_text = "ভুল অপশন। ১, ২, ৩ অথবা ৯ চাপুন।"
        operation = "mt-cont"

    return jsonify({
        "sessionId": session_id,
        "address": address,
        "message": reply_text,
        "ussdOperation": operation
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)