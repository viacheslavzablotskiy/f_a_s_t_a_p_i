# # def test_register():
# #     assert 1 == 1
# from sqlalchemy import insert, select
# from src.auth.models import role
#
# from tests.conftest import async_session_maker, client
#
#
# async def test_role():
#     async  with async_session_maker() as session:
#         stmt = insert(role).values(id=1, name="admin", permissions=None)
#         await session.execute(stmt)
#         await session.commit()
#
#         query = select(role)
#         result = await session.execute(query)
#         assert result.all() == [(1, 'admin', None)], "Role was't added"
#
#
# def test_register_user_id():
#     response = client.post("/auth/register", json={
#         "email": "rng",
#         "password": "string",
#         "is_active": True,
#         "is_superuser": False,
#         "is_verified": False,
#         "username": "string",
#         "role_id": 1
#     })
#
#     assert response.status_code == 201
#
#
