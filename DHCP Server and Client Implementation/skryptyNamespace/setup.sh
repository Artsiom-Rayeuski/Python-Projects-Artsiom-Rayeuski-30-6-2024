sysctl -w net.bridge.bridge-nf-call-arptables=0
sysctl -w net.bridge.bridge-nf-call-iptables=0
modprobe 8021q

ip netns add ns-red
ip netns exec ns-red ip link set dev lo up
ip link add vt-red type veth peer name vt-red-br
ip link set vt-red netns ns-red
ip netns exec ns-red ip link set vt-red up

ip netns add ns-green
ip netns exec ns-green ip link set dev lo up
ip link add vt-green type veth peer name vt-green-br
ip link set vt-green netns ns-green
ip netns exec ns-green ip link set vt-green up

ip netns add ns-gray
ip netns exec ns-gray ip link set dev lo up
ip link add vt-gray type veth peer name vt-gray-br
ip link set vt-gray netns ns-gray
ip netns exec ns-gray ip addr add 192.168.1.1/24 dev vt-gray
ip netns exec ns-gray ip link set vt-gray up

ip netns add ns-blue
ip netns exec ns-blue ip link set dev lo up
ip link add vt-blue type veth peer name vt-blue-br
ip link set vt-blue netns ns-blue
ip netns exec ns-blue ip addr add 192.168.2.1/24 dev vt-blue
ip netns exec ns-blue ip link set vt-blue up

ip link add br-host type bridge
ip link set dev br-host up
ip link set vt-red-br master br-host
ip link set dev vt-red-br up
ip link set vt-green-br master br-host
ip link set dev vt-green-br up
ip link set vt-gray-br master br-host
ip link set dev vt-gray-br up
ip link set vt-blue-br master br-host
ip link set dev vt-blue-br up

ip netns exec ns-red xterm -xrm 'XTerm.vt100.allowTitleOps: false' -title 'ns-red: dhcp client' -fa 'Monospace' -fs 12 -bg darkred&
ip netns exec ns-green xterm -xrm 'XTerm.vt100.allowTitleOps: false' -title 'ns-green: dhcp client' -fa 'Monospace' -fs 12 -bg darkgreen&
ip netns exec ns-gray xterm -xrm 'XTerm.vt100.allowTitleOps: false' -title 'ns-gray: dhcp server' -fa 'Monospace' -fs 12 -bg darkgrey&
ip netns exec ns-blue xterm -xrm 'XTerm.vt100.allowTitleOps: false' -title 'ns-blue: dhcpserver' -fa 'Monospace' -fs 12 -bg darkblue&
