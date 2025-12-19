module github.com/ivanphz/my-custom-caddy

go 1.25.4

replace github.com/caddyserver/forwardproxy => github.com/klzgrad/forwardproxy v0.0.0-20250118002110-d62c80d3dd2c

require (
	github.com/LeenHawk/caddy-edgeone-ip v0.1.1
	github.com/WeidiDeng/caddy-cloudflare-ip v0.0.0-20231130002422-f53b62aa13cb
	github.com/caddy-dns/tencentcloud v0.4.3
	github.com/caddyserver/caddy/v2 v2.10.2
	github.com/caddyserver/forwardproxy v0.0.0-20251013200746-bb364cc53204
	github.com/caddyserver/jsonc-adapter v0.0.0-20200325004025-825ee096306c
	github.com/fvbommel/caddy-combine-ip-ranges v0.0.1
	github.com/greenpau/caddy-security v1.1.31
	github.com/imgk/caddy-trojan v0.2.10-2
	github.com/lanrat/caddy-dynamic-remoteip v0.0.0-20231007025615-f72ed4fc7b9c
	github.com/mholt/caddy-events-exec v0.1.0
	github.com/mholt/caddy-l4 v0.0.0-20251209130418-1a3490ef786a
	github.com/mholt/caddy-ratelimit v0.1.0
	github.com/mholt/caddy-webdav v0.0.0-20250805175825-7a5c90d8bf90
	github.com/monobilisim/caddy-ip-list v0.0.0-20250818180736-cd5c45325ade
	github.com/okrc/caddy-uploadcert-tencentcloud v0.1.2
	github.com/porech/caddy-maxmind-geolocation v1.0.1
	github.com/tuzzmaniandevil/caddy-dynamic-clientip v1.0.5
	github.com/xcaddyplugins/caddy-trusted-cloudfront v0.0.0-20240604042247-0a0864e80f1c
)

require (
	cel.dev/expr v0.24.0 // indirect
	cloud.google.com/go/auth v0.16.2 // indirect
	cloud.google.com/go/auth/oauth2adapt v0.2.8 // indirect
	cloud.google.com/go/compute/metadata v0.7.0 // indirect
	dario.cat/mergo v1.0.2 // indirect
	filippo.io/edwards25519 v1.1.0 // indirect
	github.com/AndreasBriese/bbloom v0.0.0-20190825152654-46b345b51c96 // indirect
	github.com/Azure/go-ntlmssp v0.0.0-20221128193559-754e69321358 // indirect
	github.com/KimMachineGun/automemlimit v0.7.4 // indirect
	github.com/Masterminds/goutils v1.1.1 // indirect
	github.com/Masterminds/semver/v3 v3.3.1 // indirect
	github.com/Masterminds/sprig/v3 v3.3.0 // indirect
	github.com/Microsoft/go-winio v0.6.2 // indirect
	github.com/antlr4-go/antlr/v4 v4.13.1 // indirect
	github.com/aryann/difflib v0.0.0-20210328193216-ff5ff6dc229b // indirect
	github.com/beevik/etree v1.5.0 // indirect
	github.com/beorn7/perks v1.0.1 // indirect
	github.com/caddyserver/certmagic v0.25.0 // indirect
	github.com/caddyserver/zerossl v0.1.3 // indirect
	github.com/ccoveille/go-safecast v1.6.1 // indirect
	github.com/cespare/xxhash v1.1.0 // indirect
	github.com/cespare/xxhash/v2 v2.3.0 // indirect
	github.com/chzyer/readline v1.5.1 // indirect
	github.com/cloudflare/circl v1.6.1 // indirect
	github.com/coreos/go-oidc/v3 v3.14.1 // indirect
	github.com/cpuguy83/go-md2man/v2 v2.0.7 // indirect
	github.com/crewjam/httperr v0.2.0 // indirect
	github.com/crewjam/saml v0.4.14 // indirect
	github.com/dgraph-io/badger v1.6.2 // indirect
	github.com/dgraph-io/badger/v2 v2.2007.4 // indirect
	github.com/dgraph-io/ristretto v0.2.0 // indirect
	github.com/dgryski/go-farm v0.0.0-20240924180020-3414d57e47da // indirect
	github.com/dustin/go-humanize v1.0.1 // indirect
	github.com/emersion/go-sasl v0.0.0-20241020182733-b788ff22d5a6 // indirect
	github.com/emersion/go-smtp v0.21.3 // indirect
	github.com/felixge/httpsnoop v1.0.4 // indirect
	github.com/fsnotify/fsnotify v1.9.0 // indirect
	github.com/go-asn1-ber/asn1-ber v1.5.7 // indirect
	github.com/go-jose/go-jose/v3 v3.0.4 // indirect
	github.com/go-jose/go-jose/v4 v4.1.0 // indirect
	github.com/go-ldap/ldap/v3 v3.4.10 // indirect
	github.com/go-logr/logr v1.4.3 // indirect
	github.com/go-logr/stdr v1.2.2 // indirect
	github.com/go-sql-driver/mysql v1.9.2 // indirect
	github.com/golang-jwt/jwt/v4 v4.5.2 // indirect
	github.com/golang/protobuf v1.5.4 // indirect
	github.com/golang/snappy v1.0.0 // indirect
	github.com/google/btree v1.1.3 // indirect
	github.com/google/cel-go v0.26.0 // indirect
	github.com/google/s2a-go v0.1.9 // indirect
	github.com/google/uuid v1.6.0 // indirect
	github.com/googleapis/enterprise-certificate-proxy v0.3.6 // indirect
	github.com/googleapis/gax-go/v2 v2.14.2 // indirect
	github.com/gorilla/websocket v1.5.3 // indirect
	github.com/greenpau/go-authcrunch v1.1.7 // indirect
	github.com/greenpau/versioned v1.0.30 // indirect
	github.com/huandu/xstrings v1.5.0 // indirect
	github.com/imgk/memory-go v0.2.0 // indirect
	github.com/inconshreveable/mousetrap v1.1.0 // indirect
	github.com/jackc/pgpassfile v1.0.0 // indirect
	github.com/jackc/pgservicefile v0.0.0-20240606120523-5a60cdf6a761 // indirect
	github.com/jackc/pgx/v5 v5.7.5 // indirect
	github.com/jackc/puddle/v2 v2.2.2 // indirect
	github.com/jonboulle/clockwork v0.5.0 // indirect
	github.com/klauspost/compress v1.18.0 // indirect
	github.com/klauspost/cpuid/v2 v2.3.0 // indirect
	github.com/libdns/libdns v1.1.1 // indirect
	github.com/libdns/tencentcloud v1.4.3 // indirect
	github.com/manifoldco/promptui v0.9.0 // indirect
	github.com/mastercactapus/proxyprotocol v0.0.4 // indirect
	github.com/mattermost/xml-roundtrip-validator v0.1.0 // indirect
	github.com/mattn/go-colorable v0.1.14 // indirect
	github.com/mattn/go-isatty v0.0.20 // indirect
	github.com/mgutz/ansi v0.0.0-20200706080929-d51e80ef957d // indirect
	github.com/mholt/acmez/v3 v3.1.4 // indirect
	github.com/miekg/dns v1.1.68 // indirect
	github.com/mitchellh/copystructure v1.2.0 // indirect
	github.com/mitchellh/go-ps v1.0.0 // indirect
	github.com/mitchellh/reflectwalk v1.0.2 // indirect
	github.com/muhammadmuzzammil1998/jsonc v0.0.0-20200303171503-1e787b591db7 // indirect
	github.com/munnerz/goautoneg v0.0.0-20191010083416-a7dc8b61c822 // indirect
	github.com/oschwald/maxminddb-golang v1.13.1 // indirect
	github.com/pbnjay/memory v0.0.0-20210728143218-7b4eea64cf58 // indirect
	github.com/pires/go-proxyproto v0.8.1 // indirect
	github.com/pkg/errors v0.9.1 // indirect
	github.com/prometheus/client_golang v1.23.2 // indirect
	github.com/prometheus/client_model v0.6.2 // indirect
	github.com/prometheus/common v0.67.4 // indirect
	github.com/prometheus/procfs v0.19.2 // indirect
	github.com/quic-go/qpack v0.6.0 // indirect
	github.com/quic-go/quic-go v0.57.1 // indirect
	github.com/riobard/go-bloom v0.0.0-20200614022211-cdc8013cb5b3 // indirect
	github.com/rs/xid v1.6.0 // indirect
	github.com/russellhaering/goxmldsig v1.5.0 // indirect
	github.com/russross/blackfriday/v2 v2.1.0 // indirect
	github.com/shadowsocks/go-shadowsocks2 v0.1.6-0.20241020092332-e1fe9ea73740 // indirect
	github.com/shopspring/decimal v1.4.0 // indirect
	github.com/shurcooL/sanitized_anchor_name v1.0.0 // indirect
	github.com/skip2/go-qrcode v0.0.0-20200617195104-da1b6568686e // indirect
	github.com/slackhq/nebula v1.9.7 // indirect
	github.com/smallstep/certificates v0.28.4 // indirect
	github.com/smallstep/cli-utils v0.12.1 // indirect
	github.com/smallstep/linkedca v0.23.0 // indirect
	github.com/smallstep/nosql v0.7.0 // indirect
	github.com/smallstep/pkcs7 v0.2.1 // indirect
	github.com/smallstep/scep v0.0.0-20250318231241-a25cabb69492 // indirect
	github.com/smallstep/truststore v0.13.0 // indirect
	github.com/spf13/cast v1.8.0 // indirect
	github.com/spf13/cobra v1.9.1 // indirect
	github.com/spf13/pflag v1.0.7 // indirect
	github.com/stoewer/go-strcase v1.3.0 // indirect
	github.com/tailscale/tscert v0.0.0-20240608151842-d3f834017e53 // indirect
	github.com/things-go/go-socks5 v0.1.0 // indirect
	github.com/urfave/cli v1.22.17 // indirect
	github.com/zeebo/blake3 v0.2.4 // indirect
	go.etcd.io/bbolt v1.4.0 // indirect
	go.opentelemetry.io/auto/sdk v1.1.0 // indirect
	go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp v0.61.0 // indirect
	go.opentelemetry.io/otel v1.37.0 // indirect
	go.opentelemetry.io/otel/metric v1.37.0 // indirect
	go.opentelemetry.io/otel/trace v1.37.0 // indirect
	go.step.sm/crypto v0.67.0 // indirect
	go.uber.org/automaxprocs v1.6.0 // indirect
	go.uber.org/multierr v1.11.0 // indirect
	go.uber.org/zap v1.27.1 // indirect
	go.uber.org/zap/exp v0.3.0 // indirect
	go.yaml.in/yaml/v2 v2.4.3 // indirect
	golang.org/x/crypto v0.45.0 // indirect
	golang.org/x/crypto/x509roots/fallback v0.0.0-20250529171604-18228cd6f13e // indirect
	golang.org/x/exp v0.0.0-20250530174510-65e920069ea6 // indirect
	golang.org/x/mod v0.30.0 // indirect
	golang.org/x/net v0.47.0 // indirect
	golang.org/x/oauth2 v0.32.0 // indirect
	golang.org/x/sync v0.18.0 // indirect
	golang.org/x/sys v0.38.0 // indirect
	golang.org/x/term v0.37.0 // indirect
	golang.org/x/text v0.31.0 // indirect
	golang.org/x/time v0.14.0 // indirect
	golang.org/x/tools v0.39.0 // indirect
	golang.zx2c4.com/wintun v0.0.0-20230126152724-0fa3db229ce2 // indirect
	golang.zx2c4.com/wireguard v0.0.0-20250521234502-f333402bd9cb // indirect
	google.golang.org/api v0.240.0 // indirect
	google.golang.org/genproto/googleapis/api v0.0.0-20250603155806-513f23925822 // indirect
	google.golang.org/genproto/googleapis/rpc v0.0.0-20250603155806-513f23925822 // indirect
	google.golang.org/grpc v1.73.0 // indirect
	google.golang.org/grpc/cmd/protoc-gen-go-grpc v1.5.1 // indirect
	google.golang.org/protobuf v1.36.10 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
	gvisor.dev/gvisor v0.0.0-20250503011706-39ed1f5ac29c // indirect
	howett.net/plist v1.0.1 // indirect
)
