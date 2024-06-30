ip netns del ns-red
ip netns del ns-green
ip netns del ns-gray
ip netns del ns-blue

ip link del dev vt-red-br
ip link del dev vt-green-br
ip link del dev vt-gray-br
ip link del dev vt-blue-br

ip link del dev br-host
