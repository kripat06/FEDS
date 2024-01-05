//
//  ErrorView.swift
//  FedsMonitoringApp
//
//  Created by Jagdish Patel on 3/9/23.
//

import SwiftUI

struct ErrorView: View {
    @ObservedObject var parkFetcher: ParkFetcher
    var body: some View {
        VStack {
            Text("☹️").font(.system(size: 80))
            Text("Error")
        }
    }
}

struct ErrorView_Previews: PreviewProvider {
    static var previews: some View {
        ErrorView(parkFetcher: ParkFetcher())
    }
}
