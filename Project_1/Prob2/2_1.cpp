#include<bits/stdc++.h>
using namespace std;
#define int long long
signed main() {
    vector<vector<int>> g(3, vector<int>(3, 0));
    int x, y;
    for (int i = 0;i < 3;i++) {
        for (int j = 0;j < 3;j++) {
            char ch; cin >> ch;
            if (ch == 'x') {
                x = i, y = j;
                continue;
            }
            g[i][j] = ch - '0';
        }
    }
    auto encode = [&]()->int {
        int res = 0;
        for (int i = 0;i < 3;i++) {
            for (int j = 0;j < 3;j++) {
                res = res * 10 + g[i][j];
            }
        }
        // cout<<res<<endl;
        return res;
    };
    unordered_set<int> st;
    int dx[4] = { 1,0,-1,0 }, dy[4] = { 0,1,0,-1 };
    auto dfs = [&](auto self, int x, int y)->bool {
        // cout<<x<<" "<<y<<endl;
        if(encode()==123456780ll) return true;
        if (st.count(encode())) {
            return false;
        } else {
            st.insert(encode());
        }
        for (int i = 0;i < 4;i++) {
            int nx = x + dx[i], ny = y + dy[i];
            if (0 <= nx && nx <= 2 && 0 <= ny && ny <= 2) {
                swap(g[nx][ny], g[x][y]);
                if (self(self, nx, ny)) {
                    return true;
                }
                swap(g[nx][ny], g[x][y]);
            }
        }
        return false;
    };
    cout<<(dfs(dfs,x,y)?1:0)<<endl;
    return 0;
}