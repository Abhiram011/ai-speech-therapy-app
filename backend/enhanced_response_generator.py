from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import random
import os
import warnings

# Suppress warnings that can cause issues
warnings.filterwarnings("ignore", message=".*tokenizers.*")
warnings.filterwarnings("ignore", message=".*bitsandbytes.*")
warnings.filterwarnings("ignore", message=".*attention mask.*")

# Set environment variable to disable tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Use Blenderbot-400M-distill for conversation (worked best before)
BASE_MODEL = "facebook/blenderbot-400M-distill"

# Global variables to cache the model
_cached_tokenizer = None
_cached_model = None
_cached_device = None
_model_loading_failed = False

# Check if we're in test mode (skip heavy model loading)
def is_test_mode():
    return os.environ.get('TEST_MODE', 'false').lower() == 'true'

def get_response_generator():
    global _cached_tokenizer, _cached_model, _cached_device, _model_loading_failed
    
    # Return cached model if available
    if _cached_tokenizer is not None and _cached_model is not None:
        return _cached_tokenizer, _cached_model, _cached_device
    
    # If model loading previously failed, don't try again
    if _model_loading_failed:
        return None, None, None
    
    # Skip model loading in test mode
    if is_test_mode():
        # Test mode: Skipping heavy model loading
        return None, None, None
    
    try:
        # Loading Blenderbot-400M-distill model...
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        # Ensure pad_token is set to eos_token if not already set
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Force CPU for reliable operation
        device = "cpu"
        torch_dtype = torch.float32

        # Load base model
        model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL)

        # Move model to device
        model = model.to(device)
        
        model.eval()
        
        # Cache the model
        _cached_tokenizer = tokenizer
        _cached_model = model
        _cached_device = device
        
        # Blenderbot-400M-distill model loaded successfully!
        return tokenizer, model, device
        
    except Exception as e:
        # Error loading Blenderbot-400M-distill model: {e}
        # Will use fallback responses only
        _model_loading_failed = True
        return None, None, None

# Fallback responses with personalization
def get_positive_response(details):
    """Get personalized positive response based on user details"""
    topic = details.get('topic', 'this')
    time_context = details.get('time', 'recently')
    
    responses = [
        f"That's wonderful to hear about {topic}! What do you think contributed to this positive shift?",
        f"I'm really proud of your progress with {topic}. What would you like to build on from here?",
        f"You're doing a fantastic job with {topic}. What does this success tell you about your capabilities?",
        f"It sounds like you're in a good place with {topic} {time_context}. Is there anything specific you'd like to explore?",
        f"That's a significant achievement with {topic}! What did you learn about yourself through this process?"
    ]
    return random.choice(responses)

def get_neutral_response(details):
    """Get personalized neutral response based on user details"""
    topic = details.get('topic', 'this situation')
    emotion = details.get('emotion', 'how you\'re feeling')
    
    responses = [
        f"Thanks for sharing that with me about {topic}. What's been on your mind lately?",
        f"Sometimes our feelings about {topic} aren't always clear. What do you think might be contributing to {emotion} right now?",
        f"I'm here for you with {topic}. What would be most helpful for us to focus on today?",
        f"Can you tell me more about {topic}? What else comes to mind when you think about this?",
        f"Let's explore {topic} together. What aspects of this feel most important to you right now?"
    ]
    return random.choice(responses)

def get_negative_response(details):
    """Get personalized negative response based on user details"""
    topic = details.get('topic', 'this situation')
    emotion = details.get('emotion', 'these feelings')
    
    responses = [
        f"I hear how difficult {topic} is for you. What's been most challenging about this situation?",
        f"That sounds really tough with {topic}. Can you tell me more about what's contributing to {emotion}?",
        f"It's okay to feel like this about {topic}. What do you think these emotions might be trying to communicate?",
        f"Thanks for being open about {topic}. What would feel most supportive to you right now?",
        f"I'm really sorry you're going through this with {topic}. What's one small thing we could do together to help you feel a bit more supported?"
    ]
    return random.choice(responses)

# Specific responses for common requests
RELAXATION_TECHNIQUES = [
    "Here are some relaxation techniques: Deep breathing, progressive muscle relaxation, guided meditation, or taking a warm bath. Which of these sounds most appealing to you?",
    "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8. Or try progressive muscle relaxation. What feels most accessible to you?",
    "Some effective relaxation methods include mindfulness meditation, gentle stretching, or listening to calming music. Which of these resonates with you?",
    "Try box breathing: inhale for 4, hold for 4, exhale for 4, hold for 4. Or practice grounding by naming 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
    "Consider guided imagery or a body scan technique. What type of relaxation feels most natural to you?"
]

COPING_STRATEGIES = [
    "Some helpful coping strategies include journaling, talking to a friend, physical activity, or self-compassion. Which of these feels most helpful right now?",
    "Try cognitive reframing or setting small, achievable goals. What coping method has worked for you in the past?",
    "Healthy coping might include creative expression, time with loved ones, or activities that bring you joy. What feels most supportive to you?",
    "Try the STOP technique: Stop, Take a breath, Observe your thoughts and feelings, Proceed mindfully. Or practice self-soothing through your five senses. What resonates with you?",
    "Consider building a coping toolkit with activities like reading, music, walking, or calling a friend. What would you like to include?"
]

def create_therapeutic_context(user_text, sentiment_score):
    """Create a therapeutic context based on the user's input and sentiment"""
    
    # Create a more natural conversation flow
    if sentiment_score > 0.3:
        context = f"Client: {user_text}\nTherapist: I'm glad to hear you're feeling positive. "
    elif sentiment_score < -0.3:
        context = f"Client: {user_text}\nTherapist: I hear that you're struggling. "
    else:
        context = f"Client: {user_text}\nTherapist: "
    
    return context

def filter_problematic_response(response):
    """Aggressively filter out problematic responses"""
    if not response:
        return None
    
    response_lower = response.lower()
    
    # Check for self-references (the model talking about itself)
    self_refs = ['i am', "i'm a", 'i work as', 'i do', 'my job', 'my profession', 'i study', "i'm studying", 'i work for', 'analyst', 'assistant', 'software company']
    for ref in self_refs:
        if ref in response_lower:
            # Filtered out self-reference: '{ref}' in response
            return None
    
    # Check for work/profession questions
    work_questions = ['what do you do', 'what do you work', "what's your job", "what's your profession", 'what do you do for work', 'what do you do for a living', "what's your occupation"]
    for question in work_questions:
        if question in response_lower:
            # Filtered out work question: '{question}' in response
            return None
    
    # Check for random assumptions about pets, hobbies, etc.
    random_assumptions = ['what kind of pets', 'do you have pets', 'what pets', 'what hobbies', 'what do you like to do', 'what do you enjoy', 'what do you do for fun', 'what are your interests', 'do you have any pets', 'do you have a pet', 'do you have pets']
    for assumption in random_assumptions:
        if assumption in response_lower:
            # Filtered out random assumption: '{assumption}' in response
            return None
    
    # Check for generic, non-contextual responses
    generic_responses = ['hello', 'hi', 'how are you', 'that is nice', 'that is good', 'thank you', 'good job', 'well done', 'that is great']
    for generic in generic_responses:
        if generic in response_lower and len(response_lower.split()) < 5:
            # Filtered out generic response: '{generic}' in response
            return None
    
    # Check for responses that just repeat the user's input
    user_words = set(response_lower.split())
    if len(user_words) < 3:
        # Filtered out response that's too short/repetitive
        return None
    
    return response

def generate_ai_response(user_text, tokenizer, model, device):
    """Generate a therapy-specific response using Blenderbot-400M-distill with excellent prompt engineering."""
    try:
        # Analyze sentiment and content for context-aware prompting
        user_text_lower = user_text.lower()
        
        # Detect specific emotional states and content (simplified)
        if any(word in user_text_lower for word in ['kill', 'suicide', 'die', 'death', 'end it']):
            # Crisis situation
            context = "CRISIS: Someone is expressing thoughts of self-harm. Respond with immediate empathy, validation, and support. Acknowledge their pain and offer a safe space to talk."
        elif any(word in user_text_lower for word in ['sad', 'depressed', 'lonely', 'hurt', 'pain', 'crying']):
            # Negative emotions
            context = "NEGATIVE: Someone is feeling sad or in emotional pain. Respond with deep empathy, validation, and gentle support. Acknowledge their feelings as valid."
        elif any(word in user_text_lower for word in ['happy', 'excited', 'joy', 'great', 'wonderful', 'amazing', 'love']):
            # Positive emotions
            context = "POSITIVE: Someone is feeling happy or joyful. Celebrate their positive feelings, validate their happiness, and encourage them to share more about what's bringing them joy."
        elif any(word in user_text_lower for word in ['angry', 'frustrated', 'mad', 'hate', 'upset', 'annoyed']):
            # Anger/frustration
            context = "ANGER: Someone is feeling angry or frustrated. Acknowledge their feelings as valid, help them feel heard, and offer support without trying to fix the situation."
        elif any(word in user_text_lower for word in ['anxious', 'worried', 'scared', 'fear', 'nervous', 'stress']):
            # Anxiety/worry
            context = "ANXIETY: Someone is feeling anxious or worried. Provide gentle reassurance, validate their concerns, and offer support without minimizing their feelings."
        elif any(word in user_text_lower for word in ['gay', 'lesbian', 'bisexual', 'trans', 'lgbt', 'queer']):
            # Identity-related
            context = "IDENTITY: Someone is sharing something about their identity. Respond with support, validation, and acceptance. Celebrate their courage in sharing."
        else:
            # General sharing
            context = "GENERAL: Someone is sharing their thoughts or feelings. Respond with empathy, curiosity, and gentle encouragement to help them explore further."
        
        # Create a simplified but effective prompt
        prompt = (
            f"You are a supportive AI assistant helping with emotional well-being. {context}\n"
            f"Rules: Never mention yourself, focus on their feelings, use empathetic language, ask gentle questions.\n"
            f"User: {user_text}\n"
            f"Assistant:"
        )
        
        inputs = tokenizer([prompt], return_tensors='pt', padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        # About to generate response with Blenderbot-400M-distill...
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=64,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.1
            )
        # Model generation complete.
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        # Raw model output: {response}
        
        # Remove the prompt from the response if present
        if response.lower().startswith(prompt.lower()):
            response = response[len(prompt):].strip()
        
        # Filter out problematic responses
        filtered_response = filter_problematic_response(response)
        if filtered_response:
            return filtered_response.strip()
        else:
            # Response filtered out due to problematic content
            return None
    except Exception as e:
        # Error generating Blenderbot-400M-distill response: {e}
        return None

def score_response_quality(response, sentiment_score):
    """Score the quality of a response for therapist-like characteristics"""
    if not response:
        return 0
    
    score = 0
    response_lower = response.lower()
    
    # Length bonus (optimal therapeutic response length)
    if 30 <= len(response) <= 200:
        score += 4
    elif 15 <= len(response) < 30:
        score += 2
    
    # Therapeutic keywords bonus
    therapeutic_keywords = [
        'feel', 'understand', 'support', 'help', 'explore', 'process',
        'acknowledge', 'validate', 'reflect', 'share', 'experience',
        'important', 'meaningful', 'difficult', 'challenging', 'growth',
        'progress', 'journey', 'healing', 'coping', 'resilience',
        'hear', 'sounds', 'seems', 'think', 'wonder', 'curious',
        'courage', 'strength', 'valid', 'normal', 'natural'
    ]
    
    for keyword in therapeutic_keywords:
        if keyword.lower() in response_lower:
            score += 1
    
    # Question bonus (therapists ask questions)
    if '?' in response:
        score += 3
    
    # Empathy indicators
    empathy_indicators = [
        'i hear', 'i understand', 'that sounds', 'it seems', 'i can see', 
        'i imagine', 'i can imagine', 'that must be', "i'm sorry",
        "that's difficult", "that's challenging", "that's hard"
    ]
    for indicator in empathy_indicators:
        if indicator.lower() in response_lower:
            score += 2
    
    # Heavy penalty for self-references (model talking about itself)
    for ref in ['i am', "i'm a", 'i work as', 'i do', 'my job', 'my profession', 'analyst', 'assistant', 'software company']:
        if ref in response_lower:
            score -= 10  # Heavy penalty for self-references
    
    # Heavy penalty for generic responses
    generic_phrases = [
        'thank you', 'that is nice', 'good job', 'well done', 'that is good',
        "that's good", "that's nice", "that's great", "that's a good philosophy",
        "that's a good point", "that's a good way", "that's a good approach"
    ]
    for phrase in generic_phrases:
        if phrase.lower() in response_lower:
            score -= 6  # Increased penalty
    
    # Heavy penalty for repetitive responses
    words = response_lower.split()
    if len(set(words)) < len(words) * 0.6:  # Too much repetition
        score -= 5
    
    # Penalty for responses that don't match the user's emotional context
    if sentiment_score < -0.5 and any(word in response_lower for word in ['good', 'great', 'wonderful', 'excellent']):
        score -= 8  # Very inappropriate for negative sentiment
    
    # Bonus for therapeutic techniques
    if any(phrase in response_lower for phrase in ['what do you think', 'how do you feel', 'can you tell me more']):
        score += 2
    
    return score

def extract_user_details(user_text):
    """Extract specific details from user input for personalized responses (expanded coverage)"""
    user_text_lower = user_text.lower()
    details = {}

    # Expanded topic/context extraction
    if any(word in user_text_lower for word in ['job', 'work', 'career', 'employment', 'office', 'promotion', 'unemployment', 'boss', 'colleague', 'coworker', 'manager', 'layoff', 'fired', 'resign', 'burnout', 'imposter syndrome', 'overwork', 'deadline', 'workload']):
        if 'market' in user_text_lower:
            details['topic'] = 'job market'
        elif 'interview' in user_text_lower:
            details['topic'] = 'job interview'
        elif 'boss' in user_text_lower or 'manager' in user_text_lower:
            details['topic'] = 'workplace conflict'
        elif 'colleague' in user_text_lower or 'coworker' in user_text_lower:
            details['topic'] = 'workplace relationships'
        elif 'burnout' in user_text_lower:
            details['topic'] = 'burnout'
        elif 'imposter' in user_text_lower:
            details['topic'] = 'imposter syndrome'
        elif 'promotion' in user_text_lower:
            details['topic'] = 'promotion'
        elif 'unemployment' in user_text_lower or 'layoff' in user_text_lower or 'fired' in user_text_lower or 'resign' in user_text_lower:
            details['topic'] = 'job loss'
        else:
            details['topic'] = 'work stress'

    if any(word in user_text_lower for word in ['school', 'college', 'university', 'exam', 'test', 'assignment', 'homework', 'professor', 'teacher', 'class', 'grade', 'graduation', 'bullying', 'harassment']):
        if 'exam' in user_text_lower or 'test' in user_text_lower:
            details['topic'] = 'academic pressure'
        elif 'assignment' in user_text_lower or 'homework' in user_text_lower:
            details['topic'] = 'academic workload'
        elif 'bullying' in user_text_lower or 'harassment' in user_text_lower:
            details['topic'] = 'bullying or harassment'
        elif 'graduation' in user_text_lower:
            details['topic'] = 'graduation stress'
        else:
            details['topic'] = 'academic stress'

    if any(word in user_text_lower for word in ['family', 'parents', 'mom', 'dad', 'sibling', 'brother', 'sister', 'child', 'children', 'son', 'daughter', 'parenting', 'pregnancy', 'baby', 'caregiving', 'divorce', 'separation', 'stepfamily', 'adoption', 'foster']):
        if 'parents' in user_text_lower or 'mom' in user_text_lower or 'dad' in user_text_lower:
            details['topic'] = 'parent relationships'
        elif 'sibling' in user_text_lower or 'brother' in user_text_lower or 'sister' in user_text_lower:
            details['topic'] = 'sibling relationships'
        elif 'child' in user_text_lower or 'children' in user_text_lower or 'son' in user_text_lower or 'daughter' in user_text_lower:
            details['topic'] = 'parenting'
        elif 'pregnancy' in user_text_lower or 'baby' in user_text_lower:
            details['topic'] = 'pregnancy or new baby'
        elif 'caregiving' in user_text_lower:
            details['topic'] = 'caregiving'
        elif 'divorce' in user_text_lower or 'separation' in user_text_lower:
            details['topic'] = 'divorce or separation'
        elif 'adoption' in user_text_lower or 'foster' in user_text_lower:
            details['topic'] = 'adoption or foster care'
        else:
            details['topic'] = 'family dynamics'

    if any(word in user_text_lower for word in ['relationship', 'partner', 'boyfriend', 'girlfriend', 'spouse', 'husband', 'wife', 'dating', 'marriage', 'roommate', 'neighbor', 'friend', 'friendship', 'ex', 'breakup', 'divorce', 'cheating', 'infidelity', 'jealous', 'trust']):
        if 'breakup' in user_text_lower or 'divorce' in user_text_lower or 'ex' in user_text_lower:
            details['topic'] = 'relationship ending'
        elif 'marriage' in user_text_lower or 'spouse' in user_text_lower or 'husband' in user_text_lower or 'wife' in user_text_lower:
            details['topic'] = 'marriage'
        elif 'dating' in user_text_lower or 'boyfriend' in user_text_lower or 'girlfriend' in user_text_lower or 'partner' in user_text_lower:
            details['topic'] = 'dating or partnership'
        elif 'roommate' in user_text_lower:
            details['topic'] = 'roommate issues'
        elif 'neighbor' in user_text_lower:
            details['topic'] = 'neighbor issues'
        elif 'friend' in user_text_lower or 'friendship' in user_text_lower:
            details['topic'] = 'friendship'
        elif 'cheating' in user_text_lower or 'infidelity' in user_text_lower or 'jealous' in user_text_lower or 'trust' in user_text_lower:
            details['topic'] = 'trust or infidelity'
        else:
            details['topic'] = 'relationship issues'

    if any(word in user_text_lower for word in ['move', 'moving', 'immigration', 'immigrant', 'visa', 'citizenship', 'retirement', 'aging', 'elderly', 'disability', 'chronic illness', 'pain', 'disease', 'diagnosis', 'hospital', 'doctor', 'therapy', 'treatment', 'medication', 'addiction', 'alcohol', 'drugs', 'smoking', 'recovery', 'trauma', 'ptsd', 'ocd', 'adhd', 'autism', 'bereavement', 'grief', 'mourning', 'loss', 'death', 'funeral']):
        if 'move' in user_text_lower or 'moving' in user_text_lower or 'immigration' in user_text_lower or 'immigrant' in user_text_lower or 'visa' in user_text_lower or 'citizenship' in user_text_lower:
            details['topic'] = 'moving or immigration'
        elif 'retirement' in user_text_lower or 'aging' in user_text_lower or 'elderly' in user_text_lower:
            details['topic'] = 'retirement or aging'
        elif 'disability' in user_text_lower:
            details['topic'] = 'disability'
        elif 'chronic illness' in user_text_lower or 'pain' in user_text_lower or 'disease' in user_text_lower or 'diagnosis' in user_text_lower:
            details['topic'] = 'chronic illness or pain'
        elif 'hospital' in user_text_lower or 'doctor' in user_text_lower or 'therapy' in user_text_lower or 'treatment' in user_text_lower or 'medication' in user_text_lower:
            details['topic'] = 'medical treatment'
        elif 'addiction' in user_text_lower or 'alcohol' in user_text_lower or 'drugs' in user_text_lower or 'smoking' in user_text_lower or 'recovery' in user_text_lower:
            details['topic'] = 'addiction or recovery'
        elif 'trauma' in user_text_lower or 'ptsd' in user_text_lower or 'ocd' in user_text_lower or 'adhd' in user_text_lower or 'autism' in user_text_lower:
            details['topic'] = 'mental health condition'
        elif 'bereavement' in user_text_lower or 'grief' in user_text_lower or 'mourning' in user_text_lower or 'loss' in user_text_lower or 'death' in user_text_lower or 'funeral' in user_text_lower:
            details['topic'] = 'grief or loss'
        else:
            details['topic'] = 'life transition'

    # Expanded emotion extraction
    if any(word in user_text_lower for word in ['stressed', 'stress', 'overwhelmed', 'burned out', 'exhausted', 'tired', 'fatigued', 'drained']):
        details['emotion'] = 'stress'
    elif any(word in user_text_lower for word in ['anxious', 'anxiety', 'worried', 'nervous', 'panicked', 'panic', 'fear', 'afraid', 'scared', 'terrified']):
        details['emotion'] = 'anxiety'
    elif any(word in user_text_lower for word in ['depressed', 'depression', 'sad', 'down', 'hopeless', 'helpless', 'empty', 'numb', 'crying', 'tearful', 'blue']):
        details['emotion'] = 'depression'
    elif any(word in user_text_lower for word in ['angry', 'furious', 'rage', 'mad', 'irritated', 'annoyed', 'resentful', 'frustrated']):
        details['emotion'] = 'anger'
    elif any(word in user_text_lower for word in ['lonely', 'alone', 'isolated', 'abandoned', 'left out', 'unwanted']):
        details['emotion'] = 'loneliness'
    elif any(word in user_text_lower for word in ['happy', 'joy', 'excited', 'grateful', 'hopeful', 'relieved', 'peaceful', 'content', 'satisfied', 'confident', 'curious', 'proud', 'optimistic']):
        details['emotion'] = 'happiness'
    elif any(word in user_text_lower for word in ['ashamed', 'shame', 'guilty', 'guilt', 'regret', 'embarrassed', 'inadequate', 'worthless', 'useless', 'not good enough', 'failure', 'inferior']):
        details['emotion'] = 'shame'
    elif any(word in user_text_lower for word in ['bored', 'apathetic', 'indifferent', 'unmotivated', 'disinterested']):
        details['emotion'] = 'boredom'
    elif any(word in user_text_lower for word in ['motivated', 'determined', 'driven', 'inspired']):
        details['emotion'] = 'motivation'
    
    # Expanded time references
    if any(word in user_text_lower for word in ['today', 'tonight', 'this morning', 'this evening', 'right now', 'currently']):
        details['time'] = 'recent'
    elif any(word in user_text_lower for word in ['always', 'never', 'constantly', 'all the time', 'forever', 'every day', 'everyday']):
        details['time'] = 'ongoing'
    elif any(word in user_text_lower for word in ['recently', 'lately', 'past few days', 'last week', 'last month']):
        details['time'] = 'recent'
    
    return details

def get_contextual_response(user_text):
    """Get specific, contextual responses based on user input patterns with personalization"""
    user_text_lower = user_text.lower()
    details = extract_user_details(user_text)
    
    # Crisis/Suicide responses
    if any(word in user_text_lower for word in ['kill myself', 'suicide', 'want to die', 'end it all', 'no reason to live']):
        return "I hear how much pain you're in right now. You're not alone, and I'm here to listen. Can you tell me more about what's bringing you to this place? Your feelings are valid, and there are people who want to help you through this."
    
    # Job/Work stress with personalization
    if details.get('topic') == 'job market':
        return f"I understand how stressful the job market can be right now. It's such an uncertain and competitive environment, and it's completely normal to feel overwhelmed by it. What specifically about the job market is most concerning for you? Are you looking for work, or worried about job security?"
    
    if details.get('topic') == 'work stress':
        time_context = "lately" if details.get('time') == 'recent' else "recently"
        return f"Work stress can be incredibly draining, especially when it feels like it's building up {time_context}. It affects not just your professional life but your personal well-being too. What's been most challenging about your work situation {time_context}?"
    
    if details.get('topic') == 'workplace conflict':
        return "Workplace conflicts can be so stressful - they can make going to work feel like walking into a minefield. Whether it's with your boss or colleagues, these situations can really impact your mental health. What's been happening that's been so difficult?"
    
    # Academic stress with personalization
    if details.get('topic') == 'academic pressure':
        return "Academic pressure can be intense, especially when it feels like your entire future depends on your performance. Exams and tests can trigger so much anxiety and self-doubt. What's been most stressful about your academic situation lately?"
    
    if details.get('topic') == 'academic workload':
        return "The workload in school can feel absolutely overwhelming - it's like there's always another assignment, another deadline, another expectation. It can feel impossible to keep up. What's been most challenging about managing your academic workload?"
    
    # Family issues with personalization
    if details.get('topic') == 'parent relationships':
        return "Relationships with parents can be so complex - they can be our greatest source of love and support, but also our deepest wounds. What's been happening with your parents that's been affecting you? Family dynamics can be really challenging to navigate."
    
    if details.get('topic') == 'sibling relationships':
        return "Sibling relationships can be incredibly complicated - there's so much history, competition, and love all mixed together. What's been happening with your siblings that's been difficult for you?"
    
    # Relationship issues with personalization
    if details.get('topic') == 'relationship ending':
        return "The end of a relationship can feel like losing a part of yourself. It's normal to feel a mix of emotions - grief, anger, confusion, even relief. Breakups and divorces are major life transitions. How are you coping with this change?"
    
    # Specific emotions with context
    if details.get('emotion') == 'stress':
        topic = details.get('topic', 'this situation')
        return f"I can hear how stressed you're feeling about {topic}. Stress can be so overwhelming - it affects your sleep, your mood, your ability to think clearly. What's been most stressful about {topic} for you?"
    
    if details.get('emotion') == 'anxiety':
        topic = details.get('topic', 'this situation')
        return f"Anxiety about {topic} can be so overwhelming - it's like your mind and body are constantly on high alert. What's been most anxiety-provoking about {topic} recently? I'm here to listen without judgment."
    
    if details.get('emotion') == 'depression':
        time_context = "lately" if details.get('time') == 'recent' else "recently"
        return f"Depression can feel incredibly isolating and overwhelming {time_context}. It's not just feeling sad - it's a real struggle that affects every part of your life. What's been most difficult about this for you {time_context}?"
    
    if details.get('emotion') == 'loneliness':
        time_context = "lately" if details.get('time') == 'recent' else "recently"
        return f"Feeling lonely {time_context} can be one of the most painful experiences. It's not just about being physically alone - it's feeling disconnected from others. What does loneliness feel like for you right now?"
    
    if details.get('emotion') == 'anger':
        topic = details.get('topic', 'this situation')
        return f"Anger about {topic} is a powerful emotion that can feel overwhelming. It's often covering up other feelings like hurt, fear, or frustration. What's been triggering these angry feelings for you?"
    
    if details.get('emotion') == 'happiness':
        topic = details.get('topic', 'this')
        return f"It's wonderful to hear you're feeling happy about {topic}! Positive emotions are just as important to acknowledge as difficult ones. What's been bringing you this happiness? I'd love to hear more about it."
    
    # Identity and self-worth
    if any(word in user_text_lower for word in ['worthless', 'not good enough', 'failure', 'useless']):
        context = details.get('topic', 'this situation')
        return f"Those feelings of not being good enough about {context} can be so painful and persistent. It's like having a harsh critic living inside your head. Where do you think these beliefs about yourself come from?"
    
    if any(word in user_text_lower for word in ['gay', 'lesbian', 'bisexual', 'trans', 'lgbt', 'queer', 'coming out']):
        return "Sharing your identity can be both liberating and scary. It takes real courage to be authentic about who you are. How are you feeling about this aspect of yourself? Your identity is valid and worthy of celebration."
    
    # Sleep issues
    if any(word in user_text_lower for word in ['sleep', 'insomnia', 'tired', 'exhausted']):
        context = details.get('topic', 'this situation')
        return f"Sleep problems related to {context} can affect every aspect of your life - your mood, energy, concentration, even your physical health. What's been interfering with your sleep lately?"
    
    # Financial stress
    if any(word in user_text_lower for word in ['money', 'financial', 'bills', 'debt', 'poor']):
        context = details.get('topic', 'your financial situation')
        return f"Financial stress about {context} can be incredibly overwhelming - it affects your sense of security and can impact every area of your life. What's been most concerning about {context}?"
    
    # Social anxiety
    if any(word in user_text_lower for word in ['social anxiety', 'people', 'crowd', 'party', 'meeting']):
        context = details.get('topic', 'social situations')
        return f"{context.capitalize()} can feel so overwhelming when you're dealing with anxiety. It's like your mind is constantly scanning for threats. What makes {context} most challenging for you?"
    
    # Perfectionism
    if any(word in user_text_lower for word in ['perfect', 'perfectionist', 'mistake', 'failure']):
        context = details.get('topic', 'this situation')
        return f"Perfectionism about {context} can be so exhausting - it's like having impossible standards that you can never quite meet. What would it feel like to give yourself permission to be human and make mistakes?"
    
    # Return None if no specific pattern matches (will use sentiment-based fallback)
    return None

def generate_response(vader_score, roberta_score, user_text):
    """Generate a therapist-like response using contextual matching or fallback to predefined responses"""
    
    # Calculate overall sentiment score
    overall_score = vader_score
    
    # First, try to get a contextual response based on specific patterns
    contextual_response = get_contextual_response(user_text)
    if contextual_response:
        # Using contextual response based on user input patterns
        return contextual_response
    
    # Try to get AI-generated response (only if contextual matching failed)
    tokenizer, model, device = get_response_generator()
    
    if tokenizer and model:
        try:
            ai_response = generate_ai_response(user_text, tokenizer, model, device)
            if ai_response:
                # Score the AI response
                quality_score = score_response_quality(ai_response, overall_score)
                # Score the AI response
                quality_score = score_response_quality(ai_response, overall_score)
                
                # Use AI response only if it meets very high quality threshold
                if quality_score >= 10:  # Much higher threshold
                    return ai_response
                else:
                    pass  # Use fallback response
        except Exception as e:
            pass  # Use fallback response
    
    # Check for specific requests and provide targeted responses
    user_text_lower = user_text.lower()
    
    # Check for relaxation technique requests
    if any(keyword in user_text_lower for keyword in ['relax', 'relaxing', 'calm', 'stress', 'anxiety', 'breathing', 'meditation', 'technique']):
        # Using relaxation techniques response
        return random.choice(RELAXATION_TECHNIQUES)
    
    # Check for coping strategy requests
    if any(keyword in user_text_lower for keyword in ['cope', 'coping', 'deal with', 'handle', 'manage', 'strategy', 'help me']):
        # Using coping strategies response
        return random.choice(COPING_STRATEGIES)
    
    # Fallback to sentiment-based responses with personalization
    # Using enhanced fallback response
    details = extract_user_details(user_text)
    
    if overall_score > 0.3:
        return get_positive_response(details)
    elif overall_score < -0.3:
        return get_negative_response(details)
    else:
        return get_neutral_response(details) 