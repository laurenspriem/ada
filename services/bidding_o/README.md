

RESOURCE TO PATHS AND ACTIONS MAPPING

Resource        |   Post            |   Get             |   Put             |   Delete          |
-------------------------------------------------------------------------------------------------
/Item           | Create item       | List items        | Bulk update all   | Delete all items  |
                |                   |                   | items             |                   |
-------------------------------------------------------------------------------------------------
/Item/id        | Error: 405        | Show record       | If {id} exists:   | If {id} exists:   |
                |                   |                   | show record {id}  | delete record {id}|
                |                   |                   | else: error 404   | else: error 404   |
-------------------------------------------------------------------------------------------------