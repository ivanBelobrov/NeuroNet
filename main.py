def hello():
    if nn.counter('hello_repeat') > 0:
        nv.say(name='hello_repeat')
        nn.counter('hello_repeat', 0)
    else:
        if nn.counter('hello_count') == 0:
            nv.say(name='hello')
        elif nn.counter('hello_count') == 1:
            nv.say(name='hello_null')
        else:
            hang_up_null()
    with nv.listen(
            detect_policy=['confirm', 'wrong_time', 'repeat'],
            no_input_timeout=10000,
            recognition_time_out=5000
    ) as r:
        if len(r.utterance()) == 0:
            nn.counter('hello_count', '+')
            hello()
        elif r.has_entity('confirm'):
            if r.entity('confirm'):
                recommended_main()
            else:
                hang_up_wrong_time()
        elif r.has_entity('wrong_time'):
            hang_up_wrong_time()
        elif r.has_entity('repeat'):
            nn.counter('hello_repeat', 1)
            hello()
        else:
            recommended_main()


def recommended_main(recommendation=None):
    if recommendation is None:
        if nn.counter('main_repeat') > 0:
            nv.say(name='recommended_repeat')
            nn.counter('main_repeat', 0)
        elif nn.counter('recommended_default_count') == 1:
            nv.say(name='recommended_default')
        elif nn.counter('recommended_default_count') > 1:
            hang_up_null()
        elif nn.counter('recommended_null_count') == 1:
            nv.say(name='recommended_null')
        elif nn.counter('recommended_null_count') > 1:
            hang_up_null()
    elif recommendation == 'negative':
        nv.say(name='recommended_score_negative')
    elif recommendation == 'neutral':
        nv.say(name='recommended_score_neutral')
    elif recommendation == 'positive':
        nv.say(name='recommended_score_positive')
    elif recommendation == 'dont_know':
        nv.say(name='recommended_repeat_2')
    else:
        nv.say(name='recommended_main')
    with nv.listen(
            detect_policy=[
                'recommendation_score',
                'recommendation',
                'wrong_time',
                'question',
                'repeat'
            ],
            no_input_timeout=12000,
            recognition_time_out=5000
    ) as r:
        if len(r.utterance()) == 0:
            nn.counter('recommended_null_count', '+')
        elif r.has_entity('recommendation_score'):
            hang_up(r.entity('recommendation_score'))
        elif r.has_entity('recommendation'):
            recommended_main(r.entity('recommendation'))
        elif r.has_entity('repeat'):
            nn.counter('main_repeat', 1)
            recommended_main()
        elif r.has_entity('wrong_time'):
            hang_up_wrong_time()
        elif r.has_entity('question'):
            forward()
        else:
            nn.counter('recommended_default_count', '+')


def hang_up_wrong_time():
    nv.say(name='hangupwrong_time')
    nn.log(
        'call_transcription',
        nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT)
    )
    nn.log('call_duration', nv.get_call_duration())
    nn.log(
        'tag',
        'Нет времени для разговора'
    )
    # функция завершающая звонок


def hang_up_null():
    nv.say(name='hangup_null')
    nn.log(
            'call_transcription',
            nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT)
        )
    nn.log('call_duration', nv.get_call_duration())
    nn.log(
        'tag',
        'Проблемы с распознаванием'
    )
    # функция завершающая звонок


def hang_up(score):
    if score < 9:
        nv.say(name='hangup_negative')
        nn.log(
            'tag',
            'Низкая оценка'
        )
    else:
        nv.say(name='hangup_positive')
        nn.log(
            'tag',
            'Высокая оценка'
        )
    nn.log(
        'call_transcription',
        nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT)
    )
    nn.log('call_duration', nv.get_call_duration())
    # функция завершающая звонок


def forward():
    nv.say(name='forward')
    nn.log(
        'call_transcription',
        nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT)
    )
    nn.log('call_duration', nv.get_call_duration())
    nn.log(
        'tag',
        'Перевод на оператора'
    )
    # соединение со специалистом


if __name__ == '__main__':
    nn = NeuroNetLibrary(nlu_call, loop)
    nv = NeuroVoiceLibrary(nlu_call, loop)
    nn.counter('hello_count', 0)
    nn.counter('recommended_null_count', 0)
    nn.counter('hello_repeat', 0)
    nn.counter('recommended_default_count', 0)
    nn.call(msisdn='8999999999', entry_point='hello_main')
