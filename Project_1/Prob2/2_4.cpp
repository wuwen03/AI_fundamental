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

    auto h = [&]()->int {
        int t = 1, cnt = 0;
        for (int i = 0;i < 3;i++) {
            for (int j = 0;j < 3;j++) {
                if (g[i][j] == 0) continue;
                int tarx = (g[i][j] - 1) / 3, tary = (g[i][j] - 1) % 3;
                cnt += abs(tarx - i) + abs(tary - j);
            }
        }
        // cout<<cnt<<endl;
        return cnt;
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
        return (cnt & 1) == 0;
    };
    if (!check()) {
        cout << -1 << endl;
        return 0;
    }
    int start=encode();
    int tar = 123456780ll;
    map<int, pii> prev;
    unordered_set<int> st;
    typedef pair<int, pii> pip;
    priority_queue<pip, vector<pip>, greater<pip>> pq;
    pq.push(make_pair(h(), make_pair(0, encode())));
    int ans = -1;
    int cnt=0;
    while (!pq.empty()) {
        cnt++;
        auto [cost, p] = pq.top();
        auto [step, pos] = p;
        pq.pop();
        st.insert(pos);
        if (pos == tar) {
            ans = step;
            break;
        }
        auto [x, y] = decode(pos);
        for (int i = 0;i < 4;i++) {
            int nx = x + dx[i], ny = y + dy[i];
            if (0 <= nx && nx <= 2 && 0 <= ny && ny <= 2) {
                swap(g[nx][ny], g[x][y]);
                int pos = encode();
                if (st.count(pos)) {
                    swap(g[nx][ny], g[x][y]);
                    continue;
                }
                pq.push(make_pair(step + 1 + h(), make_pair(step + 1, encode())));
                prev[pos]=make_pair(-dx[i],-dy[i]);
                // cout << h() << " ";
                swap(g[nx][ny], g[x][y]);
            }
        }
        // cout << endl;
    }
    // cout<<cnt<<endl;
    // cout << ans << endl;
    auto [zx,zy]=decode(tar);
    string m="";
    while(encode()!=start) {
        auto [dx,dy]=prev[encode()];
        swap(g[zx][zy],g[zx+dx][zy+dy]);
        zx=zx+dx,zy=zy+dy;
        if(dx==-1 && dy==0) {
            m.push_back('d');
        } else if(dx==1 && dy==0) {
            m.push_back('u');
        } else if(dx==0 && dy==1) {
            m.push_back('l');
        } else {
            m.push_back('r');
        }
    }
    reverse(m.begin(),m.end());
    cout<<m<<endl;
    return 0;
}