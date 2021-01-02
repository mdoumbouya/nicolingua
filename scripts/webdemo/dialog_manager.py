import torch

DIALOG_SCHEMA = {
    "states": [
         { "id": 0, "final": False}
        ,{ "id": 1, "final": False}
        ,{ "id": 2, "final": False}
        ,{ "id": 3, "final": False}
        ,{ "id": 4, "final": False}
        ,{ "id": 51, "final": False}
        ,{ "id": 52, "final": False}
        ,{ "id": 53, "final": False}
        ,{ "id": 54, "final": False}
        ,{ "id": 55, "final": False}
        ,{ "id": 56, "final": False}
        ,{ "id": 57, "final": False}
        ,{ "id": 58, "final": False}
        ,{ "id": 59, "final": False}
        ,{ "id": 6, "final": True, "intent": "ADD_OR_UPDATE_CONTACT"}
        ,{ "id": 7, "final": False}
        ,{ "id": 8, "final": False}
        ,{ "id": 9, "final": True, "intent": "CALL_CONTACT"}
        ,{ "id": 10, "final": False}
        ,{ "id": 11, "final": True, "intent": "DELETE_CONTACT"}
    ],
    "transitions": [
         {"sid":0, "tid":1, "utt_category": "wake_word"}
        ,{"sid":1, "tid":2, "utt_category": "add_contact"}
        ,{"sid":1, "tid":3, "utt_category": "search_contact"}
        ,{"sid":2, "tid":4, "utt_category": "name"}
        ,{"sid":3, "tid":7, "utt_category": "name"}
        ,{"sid":4, "tid":51, "utt_category": "digit"}
        ,{"sid":51, "tid":52, "utt_category": "digit"}
        ,{"sid":52, "tid":53, "utt_category": "digit"}
        ,{"sid":53, "tid":54, "utt_category": "digit"}
        ,{"sid":54, "tid":55, "utt_category": "digit"}
        ,{"sid":55, "tid":56, "utt_category": "digit"}
        ,{"sid":56, "tid":57, "utt_category": "digit"}
        ,{"sid":57, "tid":58, "utt_category": "digit"}
        ,{"sid":58, "tid":59, "utt_category": "digit"}
        ,{"sid":59, "tid":6, "utt_category": "yes"}
        ,{"sid":59, "tid":0, "utt_category": "no"}
        ,{"sid":7, "tid":2, "utt_category": "update_contact"}
        ,{"sid":7, "tid":8, "utt_category": "call_contact"}
        ,{"sid":7, "tid":10, "utt_category": "delete_contact"}
        ,{"sid":8, "tid":9, "utt_category": "yes"}
        ,{"sid":8, "tid":0, "utt_category": "no"}
        ,{"sid":10, "tid":11, "utt_category": "yes"}
        ,{"sid":10, "tid":0, "utt_category": "no"}
    ],
    "initial_state": 0
}

ASR_CLASSES = [
     {"id": 0, "utt_category": "wake_word", "utt":"Savan!", "lang":"fr" }
    ,{"id": 1, "utt_category": "wake_word", "utt":"Simbon!", "lang":"ma" }
    ,{"id": 2, "utt_category": "wake_word", "utt":"Waliyou!", "lang":"pu" }
    ,{"id": 3, "utt_category": "wake_word", "utt":"Korogba!", "lang":"su" }

    ,{"id": 4, "utt_category": "add_contact", "utt":"Ajouter un contact", "lang":"fr" }
    ,{"id": 5, "utt_category": "add_contact", "utt":"Mo do bila a kono", "lang":"ma" }
    ,{"id": 6, "utt_category": "add_contact", "utt":"Bheyditu godho", "lang":"pu" }
    ,{"id": 7, "utt_category": "add_contact", "utt":"Mixi n'de sa akui", "lang":"su" }

    ,{"id": 8, "utt_category": "search_contact",    "utt":"Cherche une personne", "lang":"fr" }
    ,{"id": 9, "utt_category": "search_contact",    "utt":"Mo do gninin", "lang":"ma" }
    ,{"id": 10, "utt_category": "search_contact",   "utt":"Dhabitu godho", "lang":"pu" }
    ,{"id": 11, "utt_category": "search_contact",   "utt":"Mixi n'de fen", "lang":"su" }

    ,{"id": 12, "utt_category": "update_contact", "utt":"Modifie la", "lang":"fr" }
    ,{"id": 13, "utt_category": "update_contact", "utt":"Wo mafalin", "lang":"ma" }
    ,{"id": 14, "utt_category": "update_contact", "utt":"Wattitu mo", "lang":"pu" }
    ,{"id": 15, "utt_category": "update_contact", "utt":"Na masara", "lang":"su" }

    ,{"id": 16, "utt_category": "delete_contact", "utt":"Supprime la", "lang":"fr" }
    ,{"id": 17, "utt_category": "delete_contact", "utt":"Wo bo a kono", "lang":"ma" }
    ,{"id": 18, "utt_category": "delete_contact", "utt":"Ittu mo", "lang":"pu" }
    ,{"id": 19, "utt_category": "delete_contact", "utt":"Na ba a kui", "lang":"su" }

    ,{"id": 20, "utt_category": "call_contact", "utt":"Appele la", "lang":"fr" }
    ,{"id": 21, "utt_category": "call_contact", "utt":"Wo wolé", "lang":"ma" }
    ,{"id": 22, "utt_category": "call_contact", "utt":"Nodou mo", "lang":"pu" }
    ,{"id": 23, "utt_category": "call_contact", "utt":"Na xili", "lang":"su" }

    ,{"id": 24, "utt_category": "yes", "utt":"Oui", "lang":"fr" }
    ,{"id": 25, "utt_category": "yes", "utt":"O-hon", "lang":"ma" }
    ,{"id": 26, "utt_category": "yes", "utt":"I-hin", "lang":"pu" }
    ,{"id": 27, "utt_category": "yes", "utt":"I-yo", "lang":"su" }

    ,{"id": 28, "utt_category": "no", "utt":"Non", "lang":"fr" }
    ,{"id": 29, "utt_category": "no", "utt":"E-hen", "lang":"ma" }
    ,{"id": 30, "utt_category": "no", "utt":"O-oye", "lang":"pu" }
    ,{"id": 31, "utt_category": "no", "utt":"Adé", "lang":"su" }

    ,{"id": 32, "utt_category": "digit", "utt":"0", "lang":"fr" }
    ,{"id": 33, "utt_category": "digit", "utt":"0", "lang":"ma" }
    ,{"id": 34, "utt_category": "digit", "utt":"0", "lang":"pu" }
    ,{"id": 35, "utt_category": "digit", "utt":"0", "lang":"su" }

    ,{"id": 36, "utt_category": "digit", "utt":"1", "lang":"fr" }
    ,{"id": 37, "utt_category": "digit", "utt":"1", "lang":"ma" }
    ,{"id": 38, "utt_category": "digit", "utt":"1", "lang":"pu" }
    ,{"id": 39, "utt_category": "digit", "utt":"1", "lang":"su" }

    ,{"id": 40, "utt_category": "digit", "utt":"2", "lang":"fr" }
    ,{"id": 41, "utt_category": "digit", "utt":"2", "lang":"ma" }
    ,{"id": 42, "utt_category": "digit", "utt":"2", "lang":"pu" }
    ,{"id": 43, "utt_category": "digit", "utt":"2", "lang":"su" }

    ,{"id": 44, "utt_category": "digit", "utt":"3", "lang":"fr" }
    ,{"id": 45, "utt_category": "digit", "utt":"3", "lang":"ma" }
    ,{"id": 46, "utt_category": "digit", "utt":"3", "lang":"pu" }
    ,{"id": 47, "utt_category": "digit", "utt":"3", "lang":"su" }

    ,{"id": 48, "utt_category": "digit", "utt":"4", "lang":"fr" }
    ,{"id": 49, "utt_category": "digit", "utt":"4", "lang":"ma" }
    ,{"id": 50, "utt_category": "digit", "utt":"4", "lang":"pu" }
    ,{"id": 51, "utt_category": "digit", "utt":"4", "lang":"su" }

    ,{"id": 52, "utt_category": "digit", "utt":"5", "lang":"fr" }
    ,{"id": 53, "utt_category": "digit", "utt":"5", "lang":"ma" }
    ,{"id": 54, "utt_category": "digit", "utt":"5", "lang":"pu" }
    ,{"id": 55, "utt_category": "digit", "utt":"5", "lang":"su" }

    ,{"id": 56, "utt_category": "digit", "utt":"6", "lang":"fr" }
    ,{"id": 57, "utt_category": "digit", "utt":"6", "lang":"ma" }
    ,{"id": 58, "utt_category": "digit", "utt":"6", "lang":"pu" }
    ,{"id": 59, "utt_category": "digit", "utt":"6", "lang":"su" }

    ,{"id": 60, "utt_category": "digit", "utt":"7", "lang":"fr" }
    ,{"id": 61, "utt_category": "digit", "utt":"7", "lang":"ma" }
    ,{"id": 62, "utt_category": "digit", "utt":"7", "lang":"pu" }
    ,{"id": 63, "utt_category": "digit", "utt":"7", "lang":"su" }

    ,{"id": 64, "utt_category": "digit", "utt":"8", "lang":"fr" }
    ,{"id": 65, "utt_category": "digit", "utt":"8", "lang":"ma" }
    ,{"id": 66, "utt_category": "digit", "utt":"8", "lang":"pu" }
    ,{"id": 67, "utt_category": "digit", "utt":"8", "lang":"su" }

    ,{"id": 68, "utt_category": "digit", "utt":"9", "lang":"fr" }
    ,{"id": 69, "utt_category": "digit", "utt":"9", "lang":"ma" }
    ,{"id": 70, "utt_category": "digit", "utt":"9", "lang":"pu" }
    ,{"id": 71, "utt_category": "digit", "utt":"9", "lang":"su" }

    ,{"id": 72, "utt_category": "name", "utt":"Maman", "lang":"fr" }
    ,{"id": 73, "utt_category": "name", "utt":"N'na", "lang":"ma" }
    ,{"id": 74, "utt_category": "name", "utt":"Nene", "lang":"pu" }
    ,{"id": 75, "utt_category": "name", "utt":"N'ga", "lang":"su" }

    ,{"id": 76, "utt_category": "name", "utt":"Papa", "lang":"fr" }
    ,{"id": 77, "utt_category": "name", "utt":"N'fa", "lang":"ma" }
    ,{"id": 78, "utt_category": "name", "utt":"Baba", "lang":"pu" }
    ,{"id": 79, "utt_category": "name", "utt":"M'ba", "lang":"su" }


    ,{"id": 80, "utt_category": "name", "utt":"Fatoumata", "lang": "na"}
    ,{"id": 81, "utt_category": "name", "utt":"Mamadou", "lang": "na"}
    ,{"id": 82, "utt_category": "name", "utt":"Mariama", "lang": "na"}
    ,{"id": 83, "utt_category": "name", "utt":"Mohamed", "lang": "na"}
    ,{"id": 84, "utt_category": "name", "utt":"Kadiatou", "lang": "na"}
    ,{"id": 85, "utt_category": "name", "utt":"Ibrahima", "lang": "na"}
    ,{"id": 86, "utt_category": "name", "utt":"Aïssatou", "lang": "na"}
    ,{"id": 87, "utt_category": "name", "utt":"Aminata", "lang": "na"}
    ,{"id": 88, "utt_category": "name", "utt":"Alpha", "lang": "na"}
    ,{"id": 89, "utt_category": "name", "utt":"Thierno", "lang": "na"}
    ,{"id": 90, "utt_category": "name", "utt":"Abdoulaye", "lang": "na"}
    ,{"id": 91, "utt_category": "name", "utt":"Aboubacar", "lang": "na"}
    ,{"id": 92, "utt_category": "name", "utt":"Amadou", "lang": "na"}
    ,{"id": 93, "utt_category": "name", "utt":"Fanta", "lang": "na"}
    ,{"id": 94, "utt_category": "name", "utt":"Mariame", "lang": "na"}
    ,{"id": 95, "utt_category": "name", "utt":"Oumou", "lang": "na"}
    ,{"id": 96, "utt_category": "name", "utt":"Ousmane", "lang": "na"}
    ,{"id": 97, "utt_category": "name", "utt":"Adama", "lang": "na"}
    ,{"id": 98, "utt_category": "name", "utt":"Marie", "lang": "na"}
    ,{"id": 99, "utt_category": "name", "utt":"Moussa", "lang": "na"}
    ,{"id": 100, "utt_category": "name", "utt":"Aïssata", "lang":"na"}
    ,{"id": 101, "utt_category": "name", "utt":"Hawa", "lang":"na"}
    ,{"id": 102, "utt_category": "name", "utt":"Sékou", "lang":"na"}
    ,{"id": 103, "utt_category": "name", "utt":"Hadja", "lang":"na"}
    ,{"id": 104, "utt_category": "name", "utt":"Djénabou", "lang":"na"}
]


def single(l):
    if len(l) != 1:
        raise ValueError("List contains more than one element")
    return l[0]


def dialog_model(current_state, current_language, sorted_class_ids, class_logits):
    possible_transitions = [t for t in DIALOG_SCHEMA['transitions'] if t['sid'] == current_state]
    possible_utt_categories = set([t['utt_category'] for t in possible_transitions])
    if current_state == 0:
        possible_asr_classes = [c for c in ASR_CLASSES if c["utt_category"] in possible_utt_categories]
    else:
        possible_asr_classes = [c for c in ASR_CLASSES if c["utt_category"] in possible_utt_categories and c['lang'] in {current_language, 'na'}]

    possible_asr_class_ids = {c["id"] for c in possible_asr_classes}

    print("possible_asr_classes", possible_asr_classes)
    

    filtered_sorted_class_ids = []
    filtered_sorted_class_logits = []

    for i, c in enumerate(sorted_class_ids):
        if c in possible_asr_class_ids:
            filtered_sorted_class_ids.append(sorted_class_ids[i])
            filtered_sorted_class_logits.append(class_logits[sorted_class_ids[i]])
    
    filtered_sorted_class_probs = torch.softmax(torch.tensor(filtered_sorted_class_logits), dim=0).tolist()


    predicted_class_id = filtered_sorted_class_ids[0]
    predicted_class_prob = filtered_sorted_class_probs[0]
    predicted_class = single([c for c in possible_asr_classes if c["id"]==predicted_class_id])
    
    if current_state == 0:
        new_language = predicted_class["lang"]
    else:
        new_language = current_language

    predicted_transition = single([t for t in possible_transitions if t['utt_category'] == predicted_class['utt_category']])
    new_state_id = predicted_transition['tid']
    reply_clips = []
    dialog_context_data = get_dialog_context_data(predicted_class, predicted_transition)

    return predicted_class, predicted_class_prob, new_state_id, new_language, reply_clips, dialog_context_data


def get_dialog_context_data(predicted_class, predicted_transition):
    ctx = {}

    if predicted_transition['sid'] == 2 and predicted_transition['tid'] == 4:
        ctx['contact_new_name'] = predicted_class['utt']
    elif predicted_transition['sid'] == 3 and predicted_transition['tid'] == 7:
        ctx['contact_name'] = predicted_class['utt']
    elif predicted_transition['sid'] == 7 and predicted_transition['tid'] == 2:
        ctx['updating_contact'] = True
    elif predicted_transition['sid'] == 4 and predicted_transition['tid'] == 51:
        ctx['phone_number_digit_1'] = predicted_class['utt']
    elif predicted_transition['sid'] == 51 and predicted_transition['tid'] == 52:
        ctx['phone_number_digit_2'] = predicted_class['utt']
    elif predicted_transition['sid'] == 52 and predicted_transition['tid'] == 53:
        ctx['phone_number_digit_3'] = predicted_class['utt']
    elif predicted_transition['sid'] == 53 and predicted_transition['tid'] == 54:
        ctx['phone_number_digit_4'] = predicted_class['utt']
    elif predicted_transition['sid'] == 54 and predicted_transition['tid'] == 55:
        ctx['phone_number_digit_5'] = predicted_class['utt']
    elif predicted_transition['sid'] == 55 and predicted_transition['tid'] == 56:
        ctx['phone_number_digit_6'] = predicted_class['utt']
    elif predicted_transition['sid'] == 56 and predicted_transition['tid'] == 57:
        ctx['phone_number_digit_7'] = predicted_class['utt']
    elif predicted_transition['sid'] == 57 and predicted_transition['tid'] == 58:
        ctx['phone_number_digit_8'] = predicted_class['utt']
    elif predicted_transition['sid'] == 58 and predicted_transition['tid'] == 59:
        ctx['phone_number_digit_9'] = predicted_class['utt']
        
    return ctx