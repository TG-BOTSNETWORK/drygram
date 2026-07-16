# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import pytest
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock
from drygram import (
    DryClient, Session, BinarySession, EncryptedSession, JSONSession,
    CustomSession, SQLiteSession, MemorySession, SessionError, AuthError,
    from_rpc_error, FloodWait, PhoneMigrate, BadRequest, Unauthorized, NotFound
)


@pytest.mark.asyncio
async def test_session_string_serialization_unencrypted():
    sess = Session("my_sess_id")
    sess.api_id = 999
    sess.dc_id = 2
    sess.auth_key = b"A" * 256
    sess.user_id = 7777777
    sess.is_bot = False
    sess.device_model = "Aesthetic Client 2026"

    # Export string
    sess_str = sess.to_string()
    assert sess_str.startswith("DRY1U_")
    assert sess.version == 1
    assert len(sess.checksum) == 8

    # Import string
    imported = Session.from_string(sess_str)
    assert imported.session_id == "my_sess_id"
    assert imported.api_id == 999
    assert imported.dc_id == 2
    assert imported.auth_key == b"A" * 256
    assert imported.user_id == 7777777
    assert imported.is_bot is False
    assert imported.device_model == "Aesthetic Client 2026"
    assert imported.validate() is True
    assert imported.is_valid() is True


@pytest.mark.asyncio
async def test_session_string_serialization_encrypted():
    sess = Session("enc_sess_id")
    sess.api_id = 888
    sess.dc_id = 4
    sess.auth_key = b"B" * 256
    sess.user_id = 112233
    sess.is_bot = True

    pwd = "my_secure_password_123"
    sess_str = sess.to_string(pwd)
    assert sess_str.startswith("DRY1E_")

    # Import with correct password
    imported = Session.from_string(sess_str, pwd)
    assert imported.api_id == 888
    assert imported.dc_id == 4
    assert imported.auth_key == b"B" * 256
    assert imported.user_id == 112233
    assert imported.is_bot is True

    # Import with wrong password
    with pytest.raises(SessionError):
        Session.from_string(sess_str, "wrong_password")

    # Import without password
    with pytest.raises(SessionError):
        Session.from_string(sess_str)


@pytest.mark.asyncio
async def test_session_string_validation():
    # Corrupted string decoding failure
    with pytest.raises(SessionError):
        Session.from_string("DRY1U_corrupted_base64_$$$")
        
    # Unsupported version prefix
    with pytest.raises(SessionError):
        Session.from_string("DRY2U_xyz")


@pytest.mark.asyncio
async def test_binary_session_backend():
    bin_file = "test_bin.bin"
    if os.path.exists(bin_file):
        os.remove(bin_file)

    sess = BinarySession("bin_test", filepath=bin_file)
    sess.api_id = 123
    sess.dc_id = 3
    sess.auth_key = b"C" * 256
    sess.user_id = 12345
    await sess.save()

    # Load from file
    loaded = BinarySession("bin_test", filepath=bin_file)
    await loaded.load()
    assert loaded.api_id == 123
    assert loaded.dc_id == 3
    assert loaded.auth_key == b"C" * 256
    assert loaded.user_id == 12345

    await loaded.delete()
    assert not os.path.exists(bin_file)


@pytest.mark.asyncio
async def test_encrypted_session_backend():
    enc_file = "test_enc.enc"
    if os.path.exists(enc_file):
        os.remove(enc_file)

    pwd = "secret_passphrase"
    sess = EncryptedSession("enc_test", encryption_key=pwd, filepath=enc_file)
    sess.api_id = 456
    sess.dc_id = 1
    sess.auth_key = b"D" * 256
    sess.user_id = 98765
    await sess.save()

    # Load with correct key
    loaded = EncryptedSession("enc_test", encryption_key=pwd, filepath=enc_file)
    await loaded.load()
    assert loaded.api_id == 456
    assert loaded.dc_id == 1
    assert loaded.auth_key == b"D" * 256
    assert loaded.user_id == 98765

    # Load with wrong key
    loaded_wrong = EncryptedSession("enc_test", encryption_key="wrong_key", filepath=enc_file)
    with pytest.raises(SessionError):
        await loaded_wrong.load()

    await loaded.delete()
    assert not os.path.exists(enc_file)


@pytest.mark.asyncio
async def test_json_session_backend():
    json_file = "test_json.json"
    if os.path.exists(json_file):
        os.remove(json_file)

    sess = JSONSession("json_test", filepath=json_file)
    sess.api_id = 789
    sess.dc_id = 5
    sess.auth_key = b"E" * 256
    sess.user_id = 11111
    await sess.save()

    # Load from file
    loaded = JSONSession("json_test", filepath=json_file)
    await loaded.load()
    assert loaded.api_id == 789
    assert loaded.dc_id == 5
    assert loaded.auth_key == b"E" * 256
    assert loaded.user_id == 11111

    await loaded.delete()
    assert not os.path.exists(json_file)


@pytest.mark.asyncio
async def test_custom_session_backend():
    loaded_flag = False
    saved_flag = False
    deleted_flag = False

    async def my_load(s):
        nonlocal loaded_flag
        loaded_flag = True
        s.api_id = 777

    async def my_save(s):
        nonlocal saved_flag
        saved_flag = True

    async def my_delete(s):
        nonlocal deleted_flag
        deleted_flag = True

    sess = CustomSession("custom_test", load_callback=my_load, save_callback=my_save, delete_callback=my_delete)
    await sess.load()
    assert loaded_flag is True
    assert sess.api_id == 777

    await sess.save()
    assert saved_flag is True

    await sess.delete()
    assert deleted_flag is True


@pytest.mark.asyncio
async def test_session_lifecycle_methods():
    sess = MemorySession("life_test")
    sess.auth_key = b"F" * 256
    
    await sess.open_session()
    assert sess.last_connected > 0

    await sess.refresh_session()
    await sess.rotate_session()
    
    val_res = await sess.validate_session()
    assert val_res is True

    await sess.repair_session()
    assert sess.dc_id == 1

    await sess.migrate_session(2, "149.154.167.51", 80)
    assert sess.dc_id == 2
    assert sess.server_address == "149.154.167.51"
    assert sess.server_port == 80

    # Test backup and restore
    bk_file = "life_test.bk"
    if os.path.exists(bk_file):
        os.remove(bk_file)
    try:
        await sess.backup_session(bk_file)
        assert os.path.exists(bk_file)

        restored_sess = MemorySession("life_test_restore")
        await restored_sess.restore_session(bk_file)
        assert restored_sess.dc_id == 2
        assert restored_sess.auth_key == b"F" * 256
    finally:
        if os.path.exists(bk_file):
            os.remove(bk_file)

    # Clone / Duplicate
    cloned = await sess.clone_session()
    assert cloned.dc_id == 2
    assert cloned.session_id == "life_test_clone"

    # Authorization
    await sess.authorize()
    assert sess.auth_state == "authorized"

    await sess.deauthorize()
    assert sess.auth_state == "unauthorized"
    assert sess.auth_key is None

    # Export / Import Auth Key
    key_bytes = b"G" * 256
    await sess.import_authorization(key_bytes)
    assert sess.auth_key == key_bytes
    assert sess.auth_state == "authorized"

    exp_key = await sess.export_authorization()
    assert exp_key == key_bytes

    await sess.logout()
    assert sess.auth_key is None

    await sess.terminate()
    assert sess.auth_state == "destroyed"


@pytest.mark.asyncio
async def test_client_session_apis():
    client = DryClient("client_sess_str_test", api_id=123, api_hash="abc")
    await client.start()

    # Set up some session data
    client.session.api_id = 123
    client.session.dc_id = 3
    client.session.auth_key = b"H" * 256
    await client.session.save()

    # Export session string
    sess_str = client.export_session_string()
    assert sess_str.startswith("DRY1U_")

    # Import session string into a new client
    client2 = DryClient("client_sess_str_test_2", api_id=456, api_hash="def")
    await client2.import_session_string(sess_str)
    assert client2.session.api_id == 123
    assert client2.session.dc_id == 3
    assert client2.session.auth_key == b"H" * 256

    # Save to file
    fn = "temp_sess_str.txt"
    if os.path.exists(fn):
        os.remove(fn)
    try:
        await client.save_session_string(fn)
        assert os.path.exists(fn)

        client3 = DryClient("client_sess_str_test_3", api_id=789, api_hash="ghi")
        await client3.load_session_string(fn)
        assert client3.session.auth_key == b"H" * 256
    finally:
        if os.path.exists(fn):
            os.remove(fn)

    # Active sessions
    act = await client.get_active_sessions()
    assert len(act) == 1
    assert act[0]["hash"] == 123456789

    # Terminate and reset
    assert await client.revoke_session(123) is True
    assert await client.revoke_all_sessions() is True
    assert await client.revoke_other_sessions() is True
    assert await client.terminate_session(123) is True

    # Session information and stats
    info = await client.session_info()
    assert info["api_id"] == 123
    assert info["dc"] == 3

    cur = await client.current_session()
    assert cur["api_id"] == 123

    stats = await client.session_statistics()
    assert stats["bytes_sent"] == 1024

    # Other wrappers
    assert (await client.export_authorization(2))["id"] == 12345
    assert await client.import_authorization(123, b"bytes") is True
    assert await client.bind_temp_auth_key() is True
    assert await client.change_authorization_settings(123, True, True) is True
    assert await client.reset_web_authorizations() is True
    assert await client.reset_password() is True
    assert (await client.get_password())["has_password"] is True
    assert await client.update_password_settings("pwd", {}) is True
    assert await client.confirm_password_email("code") is True

    await client.stop()


def test_rpc_exception_parsing():
    # Flood Wait Wait parsing
    err = from_rpc_error(420, "FLOOD_WAIT_360")
    assert isinstance(err, FloodWait)
    assert err.seconds == 360
    assert err.error_code == 420

    # Phone Migrate parsing
    err2 = from_rpc_error(303, "PHONE_MIGRATE_2")
    assert isinstance(err2, PhoneMigrate)
    assert err2.migration_dc == 2
    assert err2.error_code == 303

    # BadRequest mapping
    err3 = from_rpc_error(400, "PASSWORD_HASH_INVALID")
    assert isinstance(err3, BadRequest)
    assert err3.error_message == "PASSWORD_HASH_INVALID"

    # NotFound mapping
    err4 = from_rpc_error(404, "USERNAME_NOT_OCCUPIED")
    assert isinstance(err4, NotFound)

    # Unauthorized mapping
    err5 = from_rpc_error(401, "AUTH_KEY_UNREGISTERED")
    assert isinstance(err5, Unauthorized)
