*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://127.0.0.1:8000

*** Test Cases ***
Health Check Works
    Create Session    api    ${BASE_URL}
    ${resp}=    GET On Session    api    /health
    Status Should Be    200    ${resp}
    ${body}=    Set Variable    ${resp.json()}
    Should Be Equal    ${body}[status]    ok

Get Existing Item
    Create Session    api    ${BASE_URL}
    ${resp}=    GET On Session    api    /items/1
    Status Should Be    200    ${resp}
    ${body}=    Set Variable    ${resp.json()}
    Should Be Equal As Integers    ${body}[id]    1

Get Missing Item
    Create Session    api    ${BASE_URL}
    ${resp}=    GET On Session    api    /items/999    expected_status=404
    ${body}=    Set Variable    ${resp.json()}
    Should Be Equal    ${body}[detail]    Item not found

Create And Poll Job
    Create Session    api    ${BASE_URL}
    ${payload}=    Create Dictionary    task=simulate-topology
    ${resp}=    POST On Session    api    /jobs    json=${payload}
    Status Should Be    200    ${resp}
    ${job}=    Set Variable    ${resp.json()}
    ${job_id}=    Set Variable    ${job}[job_id]

    FOR    ${i}    IN RANGE    10
        ${poll}=    GET On Session    api    /jobs/${job_id}
        ${body}=    Set Variable    ${poll.json()}
        Exit For Loop If    '${body}[state]' == 'completed'
        Sleep    1s
    END

    Should Be Equal    ${body}[state]    completed
