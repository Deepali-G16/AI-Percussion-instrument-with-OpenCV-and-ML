# AI-Percussion-instrument-with-OpenCV-and-ML
This is the code for AI drums which are played by wiggling fingers in the air. Bend of every finger tip plays a unique drum beat. 
I have synced it to the sound of percussion, but you can sync it to any musical instrument of your choice.
This project works by tracking hands through Computer vision and recognising hand gestures through machine learning model. 
I've used mediapipe machine learning model for hand_landmark recognition and OpenCV for Computer vision.
With this model, we track the position of finger tips with respect to the position of the other fingers and sync up a drum beat through our code with each finger tip.
I've linked every finger to a unique drum beat. And we can play a symphony by just wiggling our fingers in the air. 
I have synced it to tabla-drums mp3 files, you can sync it to any musical instrument of your choice.

Prerequisites : Need to install mediapipe packages on RasPi
