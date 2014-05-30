function AnswerBlock(runtime, element) {
    return {

        init: function(options) {
            // register the child validator
            $(':input', element).on('keyup', options.onChange);

            var checkmark = $('.answer-checkmark', element);
            var completed = $('.xblock-answer', element).data('completed');
            if (completed === 'True') {
                checkmark.addClass('checkmark-correct icon-ok fa-check');
            }
        },

        submit: function() {
            return $(':input', element).serializeArray();
        },

        handleSubmit: function(result) {
            var checkmark = $('.answer-checkmark', element);
            $(element).find('.message').text((result || {}).error || '');

            this.clearResult();

            if (result.completed) {
                checkmark.addClass('checkmark-correct icon-ok fa-check');
            }
            else {
                checkmark.addClass('checkmark-incorrect icon-exclamation fa-exclamation');
            }

            // TODO Modify this to be handled in mentoring.js automatically for all children.
            // This is used in workbench tests
            $(element).data('completed', result.completed);
        },

        clearResult: function() {
            var checkmark = $('.answer-checkmark', element);
            checkmark.removeClass(
                'checkmark-incorrect icon-exclamation fa-exclamation checkmark-correct icon-ok fa-check'
            );
        },

        // Returns `true` if the child is valid, else `false`
        validate: function() {

            // return true if the answer is read only
            var blockquote_ro = $('blockquote.answer.read_only', element);
            if (blockquote_ro.length > 0)
                return true;

            var input = $(':input', element),
                input_value = input.val().replace(/^\s+|\s+$/gm,''),
                answer_length = input_value.length,
                data = input.data();

            // an answer cannot be empty event if min_characters is 0
            if (_.isNumber(data.min_characters)) {
                var min_characters = _.max([data.min_characters, 1]);
                if (answer_length < min_characters) {
                    return false;
                }
            }

            return true;
        }
    }
}
