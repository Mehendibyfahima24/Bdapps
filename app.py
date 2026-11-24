import os
from flask import Flask, request, jsonify

app = Flask(__name__)

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
        "service": "SscHscBoost - SSC & HSC Study Booster"
    }), 200

@app.route("/ussd", methods=["POST"])
def ussd_webhook():
    data = request.get_json(silent=True) or request.form.to_dict() or {}

    address = data.get("address", "")
    session_id = data.get("sessionId", "")
    message = str(data.get("message", "")).strip()

    if message == "" or message.lower() in ["menu", "start", "0"]:
        reply_text = (
            "SscHscBoost (SSC & HSC)\n"
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

@app.route("/sms", methods=["POST", "GET"])
def sms_webhook():
    data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict() or {}
    incoming_msg = str(data.get("message", "")).strip().lower()

    if "hsc" in incoming_msg:
        tip = STUDY_TIPS["hsc"][0]
    elif "focus" in incoming_msg:
        tip = STUDY_TIPS["focus"][0]
    else:
        tip = STUDY_TIPS["ssc"][0]

    return jsonify({
        "status": "received",
        "reply": tip
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)