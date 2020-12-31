import torch

DIALOG_SCHEMA = {
    "states": [
         { "id": 0, "final": False}
        ,{ "id": 1, "final": False}
        ,{ "id": 2, "final": False}
        ,{ "id": 3, "final": False}
        ,{ "id": 4, "final": False}
        ,{ "id": 5, "final": False}
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
        ,{"sid":4, "tid":5, "utt_category": "digit"}
        ,{"sid":5, "tid":6, "utt_category": "yes"}
        ,{"sid":5, "tid":0, "utt_category": "no"}
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
     {"id": 0, "utt_category": "wake_word", "lang":"fr" }
    ,{"id": 1, "utt_category": "wake_word", "lang":"ma" }
    ,{"id": 2, "utt_category": "wake_word", "lang":"pu" }
    ,{"id": 3, "utt_category": "wake_word", "lang":"su" }

    ,{"id": 4, "utt_category": "add_contact", "lang":"fr" }
    ,{"id": 5, "utt_category": "add_contact", "lang":"ma" }
    ,{"id": 6, "utt_category": "add_contact", "lang":"pu" }
    ,{"id": 7, "utt_category": "add_contact", "lang":"su" }

    ,{"id": 8, "utt_category": "search_contact", "lang":"fr" }
    ,{"id": 9, "utt_category": "search_contact", "lang":"ma" }
    ,{"id": 10, "utt_category": "search_contact", "lang":"pu" }
    ,{"id": 11, "utt_category": "search_contact", "lang":"su" }

    ,{"id": 12, "utt_category": "update_contact", "lang":"fr" }
    ,{"id": 13, "utt_category": "update_contact", "lang":"ma" }
    ,{"id": 14, "utt_category": "update_contact", "lang":"pu" }
    ,{"id": 15, "utt_category": "update_contact", "lang":"su" }

    ,{"id": 16, "utt_category": "delete_contact", "lang":"fr" }
    ,{"id": 17, "utt_category": "delete_contact", "lang":"ma" }
    ,{"id": 18, "utt_category": "delete_contact", "lang":"pu" }
    ,{"id": 19, "utt_category": "delete_contact", "lang":"su" }

    ,{"id": 20, "utt_category": "call_contact", "lang":"fr" }
    ,{"id": 21, "utt_category": "call_contact", "lang":"ma" }
    ,{"id": 22, "utt_category": "call_contact", "lang":"pu" }
    ,{"id": 23, "utt_category": "call_contact", "lang":"su" }

    ,{"id": 24, "utt_category": "yes", "lang":"fr" }
    ,{"id": 25, "utt_category": "yes", "lang":"ma" }
    ,{"id": 26, "utt_category": "yes", "lang":"pu" }
    ,{"id": 27, "utt_category": "yes", "lang":"su" }

    ,{"id": 28, "utt_category": "no", "lang":"fr" }
    ,{"id": 29, "utt_category": "no", "lang":"ma" }
    ,{"id": 30, "utt_category": "no", "lang":"pu" }
    ,{"id": 31, "utt_category": "no", "lang":"su" }

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


    ,{"id": 72, "utt_category": "name", "utt":"mom", "lang":"fr" }
    ,{"id": 73, "utt_category": "name", "utt":"mom", "lang":"ma" }
    ,{"id": 74, "utt_category": "name", "utt":"mom", "lang":"pu" }
    ,{"id": 75, "utt_category": "name", "utt":"mom", "lang":"su" }

    ,{"id": 76, "utt_category": "name", "utt":"dad", "lang":"fr" }
    ,{"id": 77, "utt_category": "name", "utt":"dad", "lang":"ma" }
    ,{"id": 78, "utt_category": "name", "utt":"dad", "lang":"pu" }
    ,{"id": 79, "utt_category": "name", "utt":"dad", "lang":"su" }


    ,{"id": 80, "utt_category": "name", "utt":"fatoumata", "lang": "na"}
    ,{"id": 81, "utt_category": "name", "utt":"mamadou", "lang": "na"}
    ,{"id": 82, "utt_category": "name", "utt":"mariama", "lang": "na"}
    ,{"id": 83, "utt_category": "name", "utt":"mohamed", "lang": "na"}
    ,{"id": 84, "utt_category": "name", "utt":"kadiatou", "lang": "na"}
    ,{"id": 85, "utt_category": "name", "utt":"ibrahima", "lang": "na"}
    ,{"id": 86, "utt_category": "name", "utt":"aissatou", "lang": "na"}
    ,{"id": 87, "utt_category": "name", "utt":"aminata", "lang": "na"}
    ,{"id": 88, "utt_category": "name", "utt":"alpha", "lang": "na"}
    ,{"id": 89, "utt_category": "name", "utt":"thierno", "lang": "na"}
    ,{"id": 90, "utt_category": "name", "utt":"abdoulaye", "lang": "na"}
    ,{"id": 91, "utt_category": "name", "utt":"aboubacar", "lang": "na"}
    ,{"id": 92, "utt_category": "name", "utt":"amadou", "lang": "na"}
    ,{"id": 93, "utt_category": "name", "utt":"fanta", "lang": "na"}
    ,{"id": 94, "utt_category": "name", "utt":"mariame", "lang": "na"}
    ,{"id": 95, "utt_category": "name", "utt":"oumou", "lang": "na"}
    ,{"id": 96, "utt_category": "name", "utt":"ousmane", "lang": "na"}
    ,{"id": 97, "utt_category": "name", "utt":"adama", "lang": "na"}
    ,{"id": 98, "utt_category": "name", "utt":"marie", "lang": "na"}
    ,{"id": 99, "utt_category": "name", "utt":"moussa", "lang": "na"}
    ,{"id": 100, "utt_category": "name", "utt":"aissata", "lang":"na"}
    ,{"id": 101, "utt_category": "name", "utt":"hawa", "lang":"na"}
    ,{"id": 102, "utt_category": "name", "utt":"sekou", "lang":"na"}
    ,{"id": 103, "utt_category": "name", "utt":"hadja", "lang":"na"}
    ,{"id": 104, "utt_category": "name", "utt":"djenabou", "lang":"na"}
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

    return predicted_class_id, predicted_class_prob, new_state_id, new_language, reply_clips