from django.db import connections, router, transaction


def _get_permut(current_value, reset_value):
    # Idea from https://preshing.com/20121224/how-to-generate-a-sequence-of-unique-random-integers/
    # reset_value must be prime such that p = 3 mod 4
    residue = (current_value * current_value) % reset_value
    if current_value < reset_value / 2:
        return residue
    return reset_value - residue


def get_next_value(
        sequence_name='default',
        initial_value=1,
        reset_value=None,
        offset=0,
        *, nowait=False, using=None):
    """
    Return the next value for a given sequence.

    """
    # Inner import because models cannot be imported before their application.
    from .models import Sequence

    if reset_value is not None:
        assert initial_value < reset_value
    if offset != 0:
        assert reset_value is not None

    if using is None:
        using = router.db_for_write(Sequence)

    with transaction.atomic(using=using, savepoint=False):

        sequence, created = (
            Sequence.objects
                    .select_for_update(nowait=nowait)
                    .get_or_create(name=sequence_name,
                                   defaults={'last': initial_value})
        )

        if not created:
            sequence.last += 1
            if reset_value is not None and sequence.last >= reset_value:
                sequence.last = initial_value

        sequence.save()

        if offset == 0:
            return sequence.last

        # Return a pseudo random sequence
        return _get_permut(
            _get_permut(sequence.last, reset_value) + offset,
            reset_value
        )
