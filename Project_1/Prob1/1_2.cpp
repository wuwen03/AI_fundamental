#include<bits/stdc++.h>
using namespace std;
#define int long long
typedef long long ll;
typedef pair<int, int> pii;
const ll MOD = 998244353;
const int inf = 1e16;
void solve() {
    int n, m; cin >> n >> m;
    vector<vector<pii>> g(n + 1);
    for (int i = 0;i < m;i++) {
        int x, y, z;cin >> x >> y >> z;
        g[x].push_back(make_pair(y,z));
    }
    vector<int> dis(n+1,inf),vis(n+1,0);
    dis[1]=0;
    for(int i=0;i<n;i++) {
        int tar=0;
        for(int i=1;i<=n;i++) {
            if(vis[i]) continue;
            if(tar==0 || dis[tar]>dis[i]) {
                tar=i;
            }
        }
        vis[tar]=1;
        for(auto [u,d]:g[tar]) {
            dis[u]=min(dis[u],dis[tar]+d);
        }
    }
    cout<<(dis[n]==inf?-1:dis[n])<<endl;
    // for(int i=1;i<=n;i++) {
    //     cout<<(dis[i]==inf?-1:dis[i])<<" ";
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