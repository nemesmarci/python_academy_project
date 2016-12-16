class Review(object):
    def __init__(self):
        self._submission = ''
        self._review_request1 = ''
        self._review_request2 = ''
        self._review_response1 = ''
        self._review_response2 = ''
        self._evaluation_result = ''

    def set_submission(self, message):
        if not self._submission and message:
            self._submission = message
        else:
            raise ValueError('Invalid request')

    def set_review_request_1(self, message):
        if not self._review_request1 and self._submission and message:
            self._review_request1 = message
        else:
            raise ValueError('Invalid request')

    def set_review_request_2(self, message):
        if not self._review_request2 and self._review_request1 and message:
            self._review_request2 = message
        else:
            raise ValueError('Invalid request')

    def set_review_response_1(self, message):
        if not self._review_response1 and self._review_request1 and message:
            self._review_response1 = message
        else:
            raise ValueError('Invalid request')

    def set_review_response_2(self, message):
        if not self._review_response2 and self._review_request2 and message:
            self._review_response2 = message
        else:
            raise ValueError('Invalid request')

    def set_evaluation_result(self, message):
        if not self._evaluation_result and self._review_response1 \
                and self._review_response2 and message:
            self._evaluation_result = message
        else:
            raise ValueError('Invalid request')
