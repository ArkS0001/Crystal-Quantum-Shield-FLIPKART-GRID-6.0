local function scramble_token(token)
    return token:reverse()  -- Example: Simple reversal of the token
end

local auth_header = ngx.req.get_headers()["Authorization"]

if auth_header then
    local token = string.match(auth_header, "Bearer%s+(.+)")
    if token then
        local scrambled_token = scramble_token(token)
        ngx.req.set_header("Authorization", "Bearer " .. scrambled_token)
    end
end
