from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text

from src.presentation.telegram_admin.interactor import TelegramAdminInteractor
from src.application.commands.add_movie.command import AddMovieCommand
from . import templates
from . import keyboards
from . import callbacks


__all__ = ("setup_handlers",)


def setup_handlers(router: Router) -> None:
    router.message.register(
        add_movie_command_handler,
        Command("add_movie")
    )
    router.message.register(
        add_movie_command_handler_set_title,
        AddMovieStatesGroup.set_title
    )
    router.message.register(
        add_movie_command_handler_set_release_date,
        AddMovieStatesGroup.set_release_date
    )
    router.message.register(
        add_movie_command_handler_set_poster,
        AddMovieStatesGroup.set_poster
    )
    router.callback_query.register(
        add_movie_command_handler_set_genres,
        callbacks.SetGenresCallbackFactory.filter(F.action == "add")
    )
    router.callback_query.register(
        add_movie_command_handler_remove_genres,
        callbacks.SetGenresCallbackFactory.filter(F.action == "remove")
    )
    router.callback_query.register(
        add_movie_command_handler_set_genres_done,
        callbacks.SetGenresCallbackFactory.filter(F.action == "done")
    )
    router.callback_query.register(
        add_movie_command_handler_set_status,
        callbacks.SetStatusCallbackFactory.filter()
    )
    router.callback_query.register(
        add_movie_command_handler_set_mpaa,
        callbacks.SetMpaaCallbackFactory.filter()
    )
    router.callback_query.register(
        add_movie_command_handler_confirm,
        callbacks.ConfirmCallbackFactory.filter(F.confirm == True)
    )
    router.callback_query.register(
        add_movie_command_handler_cancel,
        callbacks.ConfirmCallbackFactory.filter(F.confirm == False)
    )


class AddMovieStatesGroup(StatesGroup):

    set_title = State()
    set_release_date = State()
    set_poster = State()
    set_status = State()
    set_genres = State()
    set_mpaa = State()

    confirm = State()


async def add_movie_command_handler(
    messsage: Message,
    state: FSMContext
) -> None:
    await messsage.answer(templates.set_title())
    await state.set_state(AddMovieStatesGroup.set_title)


async def add_movie_command_handler_set_title(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer(templates.set_release_date())
    await state.update_data(title=message.text)
    await state.set_state(AddMovieStatesGroup.set_release_date)


async def add_movie_command_handler_set_release_date(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer(templates.set_poster())
    await state.update_data(release_date="2008.02.28")
    await state.set_state(AddMovieStatesGroup.set_poster)


async def add_movie_command_handler_set_poster(
    message: Message,
    state: FSMContext,
) -> None:
    await message.answer(
        text=templates.set_genres(),
        reply_markup=keyboards.set_genres()
    )
    await state.update_data(poster=None)
    await state.set_state(AddMovieStatesGroup.set_genres)


async def add_movie_command_handler_set_genres(
    callback: CallbackQuery,
    callback_data: callbacks.SetGenresCallbackFactory,
    state: FSMContext
) -> None:
    state_data = await state.get_data()
    genres = state_data.get("genres", [])
    genres.append(callback_data.value)

    await state.update_data(genres=genres)
    await callback.message.edit_text(
        text=templates.set_genres(genres),
        reply_markup=keyboards.set_genres(genres)
    )
    await callback.answer()


async def add_movie_command_handler_remove_genres(
    callback: CallbackQuery,
    callback_data: callbacks.SetGenresCallbackFactory,
    state: FSMContext
) -> None:
    state_data = await state.get_data()

    genres = state_data.get("genres", [])
    if callback_data.value in genres:
        genres.remove(callback_data.value)
    
    await state.update_data(genres=genres)
    await callback.message.edit_text(
        text=templates.set_genres(genres),
        reply_markup=keyboards.set_genres(genres)
    )
    await callback.answer()
    

async def add_movie_command_handler_set_genres_done(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(AddMovieStatesGroup.set_status)
    await callback.message.edit_text(
        text=templates.set_status(),
        reply_markup=keyboards.set_status()
    )
    await callback.answer()


async def add_movie_command_handler_set_status(
    callback: CallbackQuery,
    callback_data: callbacks.SetStatusCallbackFactory,
    state: FSMContext
) -> None:
    await state.update_data(status=callback_data.value)
    await callback.message.edit_text(
        text=templates.set_mpaa(),
        reply_markup=keyboards.set_mpaa()
    )
    await callback.answer()


async def add_movie_command_handler_set_mpaa(
    callback: CallbackQuery,
    callback_data: callbacks.SetMpaaCallbackFactory,
    state: FSMContext
) -> None:
    await state.update_data(mpaa=callback_data.value)
    await callback.message.edit_text(
        text=templates.confirm(),
        reply_markup=keyboards.confirm()
    )
    await callback.answer()


async def add_movie_command_handler_confirm(
    callback: CallbackQuery,
    state: FSMContext,
    interactor: TelegramAdminInteractor
) -> None:
    state_data = await state.get_data()

    command = AddMovieCommand(**state_data)
    interactor.handle_add_movie_command(command)

    await state.clear()
    await callback.answer("Movie added")


async def add_movie_command_handler_cancel(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await state.clear()
    await callback.answer("Movie adding canceled")

    