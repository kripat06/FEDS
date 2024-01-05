//
//  LoadingView.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/9/23.
//

import SwiftUI

struct LoadingView: View {
    var body: some View {
        VStack {
            Text("🌍").font(.system(size: 80))
            ProgressView()
            Text("Loading all parks...").foregroundColor(.gray)
        }
    }
}

struct LoadingView_Previews: PreviewProvider {
    static var previews: some View {
        LoadingView()
    }
}
