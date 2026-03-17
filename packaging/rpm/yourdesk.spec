Name:           yourdesk
Version:        1.0.0
Release:        1%{?dist}
Summary:        AnyDesk-like Linux remote support toolkit
License:        MIT
BuildArch:      noarch
Requires:       python3, python3-fastapi, python3-uvicorn, python3-pydantic, x11vnc, python3-websockify

%description
YourDesk provides broker + host/join CLI tooling for remote desktop support.

%files
%license LICENSE
%doc README.md docs/

%changelog
* Mon Jan 01 2026 YourDesk Team <support@yourdesk.local> - 1.0.0-1
- Initial package
