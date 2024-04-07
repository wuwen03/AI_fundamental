#include<bits/stdc++.h>
using namespace std;
#define int long long
typedef long long ll;
typedef pair<int, int> pii;
const ll MOD = 998244353;
const int inf = 1e16;

void solve() {
    int n, m; cin >> n >> m;
    // int s; cin>>s;
    vector<int> dis(n + 1, inf);
    vector<int> vis(n + 1, 0);
    vector<vector<pii>> g(n + 1);
    for (int i = 0;i < m;i++) {
        int x, y, z;
        cin >> x >> y >> z;
        g[x].push_back(make_pair(y, z));
    }
    priority_queue<pii, vector<pii>, greater<pii>> pq;
    pq.push(make_pair(0, 1));
    dis[1] = 0;
    // pq.push(make_pair(0,s));
    // dis[s]=0;
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        // vis[u]=0;
        if (vis[u]) continue;
        for (auto [v, l] : g[u]) {
            if (dis[u] + l >= dis[v]) continue;
            dis[v] = dis[u] + l;
            pq.push(make_pair(dis[v], v));
        }
        vis[u] = 1;
    }
    cout << (dis[n] == inf ? -1 : dis[n]) << endl;
    // for(int i=1;i<=n;i++) {
    // cout<<(dis[i]==inf?-1:dis[i])<<" ";
    // }
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
3 3
1 2 2
2 3 1
1 3 4
*/