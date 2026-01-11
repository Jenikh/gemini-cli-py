# @license
# Copyright 2025 Google LLC
# SPDX-License-Identifier: Apache-2.0

import asyncio

class AbortError(Exception):
    """Custom error for aborted operations."""
    def __init__(self, message="Aborted"):
        self.message = message
        super().__init__(self.message)

def create_abort_error() -> AbortError:
    """Factory to create a standard abort error."""
    return AbortError()

async def delay(ms: int, signal: asyncio.Event = None) -> None:
    """
    Waits for a given duration unless an abort signal (asyncio.Event) is set.

    Args:
        ms: Delay duration in milliseconds.
        signal: Optional asyncio.Event to signal cancellation early.
    """
    if not signal:
        await asyncio.sleep(ms / 1000)
        return

    if signal.is_set():
        raise create_abort_error()

    # Create tasks for the sleep and for waiting on the signal
    sleep_task = asyncio.create_task(asyncio.sleep(ms / 1000))
    signal_task = asyncio.create_task(signal.wait())

    # Wait for the first task to complete
    done, pending = await asyncio.wait(
        [sleep_task, signal_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    # Clean up by cancelling the other pending task
    for task in pending:
        task.cancel()

    # If the signal task finished, it means we were aborted
    if signal_task in done:
        raise create_abort_error()
    
    # Otherwise, the sleep finished successfully