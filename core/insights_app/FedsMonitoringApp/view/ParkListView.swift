//
//  ParkListView.swift
//  FedsMonitoringApp
//
//  Created by Jagdish Patel on 3/9/23.
//

import SwiftUI

struct ParkListView: View {

    @StateObject var viewModel = ParkFetcher()

    var body: some View {
        VStack {
            Text("FEDS Monitored Parks")
                .font(.system(size: 45))
                .bold()
                .foregroundColor(.white)
            NavigationStack {
                ScrollView {
                    VStack {
                        ForEach(viewModel.parks) { park in
                            NavigationLink(destination: ParkDetailView(park: park)) {
                                ParkRow(park: park)
                            }
                        }
                    }
                }.onAppear(perform: viewModel.fetchParks)
            }
        }
    }
}

struct ParkListView_Previews: PreviewProvider {
    static var previews: some View {
        ParkListView()
    }
}
