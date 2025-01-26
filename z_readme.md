pip install -r requirements.txt
python main.py

check what design pattern can be used

improve the code structure and maintainability

Observer Pattern - For handling anime updates and notifications
Command Pattern - For handling different bot commands
State Pattern - For managing conversation states
Factory Pattern - For creating different types of keyboard markups

# debug 1
if you found the conversation is not triggered, check callback_data in keyboards.py


# debug 2
fuck
must add the callback handler after the conversation handler
otherwise, the conversation handler will not be triggered.....

# debug 3
uncomment for debug
self.button_callback_manager.register_callback(self.error_button_callback, None)
