//go:build tools
package main
import (
  _ "github.com/caddyserver/caddy/v2"
  _ "github.com/caddyserver/forwardproxy"
  _ "github.com/imgk/caddy-trojan"
  _ "github.com/mholt/caddy-l4"
  _ "github.com/fvbommel/caddy-combine-ip-ranges"
  _ "github.com/LeenHawk/caddy-edgeone-ip"
  _ "github.com/monobilisim/caddy-ip-list"
  _ "github.com/WeidiDeng/caddy-cloudflare-ip"
  _ "github.com/xcaddyplugins/caddy-trusted-cloudfront"
)
