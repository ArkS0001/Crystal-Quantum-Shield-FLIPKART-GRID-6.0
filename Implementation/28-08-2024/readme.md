git clone https://luajit.org/git/luajit.git

E:\Lua\luajit\src>msvcbuild
You must open a "Visual Studio Command Prompt" to run this script
E:\Lua\luajit\src>cd..

E:\Lua\luajit>mingw32-make
"==== Building LuaJIT 2.1 ===="
mingw32-make -C src
mingw32-make[1]: Entering directory 'E:/Lua/luajit/src'
"HOSTCC    host/minilua.o"
"HOSTLINK  host/minilua.exe"
"VERSION   luajit.h"
"DYNASM    host/buildvm_arch.h"
"HOSTCC    host/buildvm.o"
"HOSTCC    host/buildvm_asm.o"
"HOSTCC    host/buildvm_peobj.o"
"HOSTCC    host/buildvm_lib.o"
"HOSTCC    host/buildvm_fold.o"
"HOSTLINK  host/buildvm.exe"
"BUILDVM   lj_vm.o"
"CC        lj_assert.o"
"CC        lj_gc.o"
"BUILDVM   lj_ffdef.h"
"CC        lj_err.o"
"CC        lj_char.o"
"BUILDVM   lj_bcdef.h"
"CC        lj_bc.o"
"CC        lj_obj.o"
"CC        lj_buf.o"
"CC        lj_str.o"
"CC        lj_tab.o"
"CC        lj_func.o"
"CC        lj_udata.o"
"CC        lj_meta.o"
"CC        lj_debug.o"
"CC        lj_prng.o"
"CC        lj_state.o"
"CC        lj_dispatch.o"
"CC        lj_vmevent.o"
"CC        lj_vmmath.o"
"CC        lj_strscan.o"
"CC        lj_strfmt.o"
"CC        lj_strfmt_num.o"
"CC        lj_serialize.o"
"CC        lj_api.o"
"CC        lj_profile.o"
"CC        lj_lex.o"
"CC        lj_parse.o"
"CC        lj_bcread.o"
"CC        lj_bcwrite.o"
"CC        lj_load.o"
"CC        lj_ir.o"
"CC        lj_opt_mem.o"
"BUILDVM   lj_folddef.h"
"CC        lj_opt_fold.o"
"CC        lj_opt_narrow.o"
"CC        lj_opt_dce.o"
"CC        lj_opt_loop.o"
"CC        lj_opt_split.o"
"CC        lj_opt_sink.o"
"CC        lj_mcode.o"
"CC        lj_snap.o"
"CC        lj_record.o"
"CC        lj_crecord.o"
"BUILDVM   lj_recdef.h"
"CC        lj_ffrecord.o"
"CC        lj_asm.o"
"CC        lj_trace.o"
"CC        lj_gdbjit.o"
"CC        lj_ctype.o"
"CC        lj_cdata.o"
"CC        lj_cconv.o"
"CC        lj_ccall.o"
"CC        lj_ccallback.o"
"CC        lj_carith.o"
"CC        lj_clib.o"
"CC        lj_cparse.o"
"CC        lj_lib.o"
"CC        lj_alloc.o"
"CC        lib_aux.o"
"BUILDVM   lj_libdef.h"
"CC        lib_base.o"
"CC        lib_math.o"
"CC        lib_bit.o"
"CC        lib_string.o"
"CC        lib_table.o"
"CC        lib_io.o"
"CC        lib_os.o"
"CC        lib_package.o"
"CC        lib_debug.o"
"CC        lib_jit.o"
"CC        lib_ffi.o"
"CC        lib_buffer.o"
"CC        lib_init.o"
"DYNLINK   lua51.dll"
"CC        luajit.o"
"BUILDVM   jit/vmdef.lua"
"LINK      luajit.exe"
"OK        Successfully built LuaJIT"
mingw32-make[1]: Leaving directory 'E:/Lua/luajit/src'
"==== Successfully built LuaJIT 2.1 ===="

```
To implement token scrambling in a reverse proxy on a Windows environment using NGINX and Lua, follow these steps:
1. Set Up NGINX with Lua Support on Windows
Download and Install NGINX

    Download NGINX for Windows:
        Go to the NGINX download page and download the Windows version.

    Install NGINX:
        Extract the downloaded ZIP file to a directory, e.g., C:\nginx.

    Verify NGINX Installation:
        Open Command Prompt, navigate to the NGINX directory, and run:

        bash

        cd C:\nginx
        start nginx

        Open a browser and navigate to http://localhost/ to verify that NGINX is running.

Install LuaJIT and Lua Modules

To use Lua with NGINX on Windows, you’ll need LuaJIT or Lua with the ngx_lua module.

    Download LuaJIT:
        Download the LuaJIT binary for Windows.
        Extract the LuaJIT files to a directory, e.g., C:\luajit.

    Add LuaJIT to the Path:
        Add C:\luajit to your system’s PATH environment variable.

    Download LuaRocks (optional):
        LuaRocks is a package manager for Lua. You can download it here, though it's optional if you want to install additional Lua modules.

2. Create the Lua Script for Token Scrambling

Create a Lua script to scramble the tokens.

    Create the Lua Script:
        Create a new file named token_scramble.lua in the NGINX directory, e.g., C:\nginx\scripts\token_scramble.lua.

    lua

    local function scramble_token(token)
        -- Example: Simple reversal of the token
        return token:reverse()
    end

    -- Modify Authorization Header
    local auth_header = ngx.req.get_headers()["Authorization"]

    if auth_header then
        -- Extract the token assuming it's in the format "Bearer <token>"
        local token = string.match(auth_header, "Bearer%s+(.+)")
        if token then
            local scrambled_token = scramble_token(token)
            ngx.req.set_header("Authorization", "Bearer " .. scrambled_token)
        end
    end

3. Configure NGINX to Use the Lua Script

Now, configure NGINX to execute the Lua script before proxying the request.

    Edit the NGINX Configuration:
        Open the nginx.conf file located in the C:\nginx\conf\ directory.
        Add the following configuration:

    nginx

    http {
        lua_package_path "C:/nginx/scripts/?.lua;;";  # Ensure Lua can find your script

        server {
            listen 80;
            server_name localhost;

            location / {
                # Execute the Lua script before passing the request to the backend
                access_by_lua_file C:/nginx/scripts/token_scramble.lua;

                # Proxy to your backend server
                proxy_pass http://127.0.0.1:5000;  # Replace with your backend server address
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
    }

4. Restart NGINX

After editing the nginx.conf file, restart NGINX to apply the changes.

    Restart NGINX:
        Open Command Prompt and run:

        bash

        nginx -s reload

5. Testing the Setup

    Start the Backend Server (if you haven't already):
        Ensure your backend server (e.g., Flask) is running and accessible at the address specified in the proxy_pass directive.

    Send a Request:
        Send an HTTP request with an Authorization header to the NGINX server, and check that the token is scrambled before it reaches the backend.

6. Security and Customization

    Custom Scrambling Logic: Modify the scramble_token function in the Lua script to implement more complex obfuscation.
    Encryption: Consider implementing encryption if security is a major concern.

This setup will enable token scrambling in the reverse proxy on a Windows environment, adding an additional layer of security or obfuscation before forwarding requests to the backend.

```
