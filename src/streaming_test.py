from talking_pi import create_talking_pi
import sys


if len(sys.argv) < 2:
    text = "Respond to me in about 4 sentences"
else:
    text = sys.argv[1]

pi = create_talking_pi()
pi.stream_response_to_question(text)
