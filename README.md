# Kastro_qa_guru_api_reqres_automation_test_hw19

1. Написать еще 10 автотестов на API (https://reqres.in/) на валидацию схем ответа.
2. Применить знания из лекции к своему проекту.
3. Добавить логирование каждого request-curl и response в allure-attachment.
4. Добавить вывод статус-кода ответа в начало сообщения с curl.
5. В логировании ответа в аллюр репорт сделать универсальную обработку response json и text, 
   зависимости от того что пришло в ответе.

Start one test:

pytest tests/test_reqres.py::test_patch

Start all tests:

pytest .
