#include<bits/stdc++.h>
using namespace std;
typedef pair<int, int> pii;
int dx[4] = { 1,0,-1,0 }, dy[4] = { 0,1,0,-1 };

int main() {
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
    auto decode = [&](int pos) -> pii {
        pii z;
        for (int i = 2;i >= 0;i--) {
            for (int j = 2;j >= 0;j--) {
                g[i][j] = pos % 10;
                if (!g[i][j]) {
                    z = make_pair(i, j);
                }
                pos /= 10;
            }
        }
        return z;
    };
    auto check = [&]() -> bool {
        vector<int> v;
        for (int i = 0;i < 3;i++) {
            for (int j = 0;j < 3;j++) {
                v.push_back(g[i][j]);
            }
        }
        int cnt = 0;
        for (int i = 0;i < 9 - 1;i++) {
            for (int j = i + 1;j < 9;j++) {
                if (v[j] == 0) continue;
                if (v[j] < v[i]) {
                    cnt++;
                }
            }
        }
        // cout<<"cnt"<<cnt<<endl;
        return (cnt & 1) == 0;
    };
    if (!check()) {
        cout << -1 << endl;
        return 0;
    }
    int tar = 123456780ll;
    if (tar == encode()) {
        cout << 0 << endl;
        return 0;
    }
    set<int> st;
    queue<int> que;
    int ans = 0;
    que.push(encode());
    st.insert(encode());
    int cnt=0;
    while (!que.empty()) {
        queue<int> q;
        cnt++;
        while (!que.empty()) {
            int pos = que.front();
            if (pos == tar) {
                goto a1;
            }
            que.pop();
            auto [x, y] = decode(pos);
            for (int i = 0;i < 4;i++) {
                int nx = x + dx[i], ny = y + dy[i];
                if (0 <= nx && nx <= 2 && 0 <= ny && ny <= 2) {
                    swap(g[nx][ny], g[x][y]);
                    if (st.count(encode())) {
                        swap(g[nx][ny], g[x][y]);
                        continue;
                    }
                    q.push(encode());
                    st.insert(encode());
                    swap(g[nx][ny], g[x][y]);
                }
            }
        }
        ans++;
        swap(que, q);
    }
a1:
// cout<<cnt<<endl;
cout << (ans == 0 ? -1 : ans) << endl;
    return 0;
}