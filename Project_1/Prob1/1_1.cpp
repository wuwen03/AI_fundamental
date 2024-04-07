#include<bits/stdc++.h>
using namespace std;
#define int long long
#define ll long long
const int inf = 1e16;
void solve() {
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int i = 0;i < m;i++) {
        int u, v;cin >> u >> v;
        g[u].push_back(v);
    }
    vector<ll> dis(n + 1, inf);
    queue<int> que;
    que.push(1);
    dis[1] = 0;
    while (!que.empty()) {
        int u = que.front();
        que.pop();
        for (auto& v : g[u]) {
            if (u == v) continue;
            if (dis[v] != inf) continue;
            dis[v] = dis[u] + 1;
            que.push(v);
        }
    }
    cout << (dis[n] == inf ? -1 : dis[n]) << endl;
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int t = 1;
    // cin >> t;
    while (t--) solve();
    return 0;
}
/*
4 5
1 2
2 3
3 4
1 3
1 4
1


*/