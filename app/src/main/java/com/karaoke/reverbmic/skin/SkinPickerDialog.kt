package com.karaoke.reverbmic.skin

import android.graphics.Bitmap
import android.graphics.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.caverock.androidsvg.SVG
import com.karaoke.reverbmic.ThemeState
import com.karaoke.reverbmic.bestTextColorFor
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

private val PanelBg = Color(0xFF1A1D26)
private val RowBg = Color(0xFF232733)
private val Dim = Color(0xFF9AA0B0)

/** Satu baris daftar: UI klasik, skin bawaan, atau skin repo. [repo] == null untuk dua yang pertama. */
private class SkinRow(
    val id: String, val title: String, val sub: String,
    val repo: SkinRepository.RepoSkin?, val status: SkinRepository.Status?,
)

/**
 * Pemilih skin: UI klasik, skin bawaan (assets), dan skin repo SKIN-MIXER-HP (UNDUH / PERBARUI / PAKAI).
 * Offline: daftar dari cache index / skin terpasang. Skin gagal diunduh/divalidasi -> pilihan lama tetap.
 */
@Composable
fun SkinPickerDialog(onDismiss: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val rows = remember { mutableStateListOf<SkinRow>() }
    var loading by remember { mutableStateOf(true) }
    var message by remember { mutableStateOf("") }
    var busyId by remember { mutableStateOf<String?>(null) }
    var selected by remember { mutableStateOf(SkinManager.selectedId(context)) }
    var refreshKey by remember { mutableStateOf(0) }

    LaunchedEffect(refreshKey) {
        loading = true
        val idx = SkinRepository.fetchIndex(context)
        val list = ArrayList<SkinRow>()
        list.add(SkinRow(SkinManager.CLASSIC_ID, "UI Klasik", "tampilan knob bawaan tanpa skin", null, null))
        list.add(SkinRow(SkinManager.BUNDLED_ID, "Skin bawaan", "ada di dalam APK (offline)", null, null))
        val known = HashSet<String>()
        withContext(Dispatchers.IO) {
            for (s in idx.skins) {
                known.add(s.id)
                list.add(SkinRow(s.id, s.name, "v${s.version} · ${s.author}", s, SkinRepository.status(context, s)))
            }
            // terpasang tapi tidak ada di index (mis. offline tanpa cache index)
            for (s in SkinRepository.installedSkins(context)) if (known.add(s.id))
                list.add(SkinRow(s.id, s.name, "v${s.version} · ${s.author}", s, SkinRepository.Status.INSTALLED))
        }
        rows.clear(); rows.addAll(list)
        message = when {
            idx.error == null -> "${idx.skins.size} skin di repo"
            idx.skins.isNotEmpty() -> "Offline — daftar dari cache (${idx.skins.size} skin)"
            else -> "Offline — hanya skin terpasang"
        }
        loading = false
    }

    fun useId(id: String) {
        scope.launch {
            busyId = id
            val ok = SkinManager.useSkin(context, id)
            busyId = null
            selected = SkinManager.selectedId(context)
            if (ok) onDismiss() else message = "Gagal memakai skin '$id' — pilihan sebelumnya dipertahankan"
        }
    }

    fun install(s: SkinRepository.RepoSkin) {
        scope.launch {
            busyId = s.id
            message = "Mengunduh ${s.name}…"
            val err = SkinRepository.install(context, s)
            busyId = null
            if (err != null) { message = "Gagal: $err"; return@launch }
            useId(s.id)
        }
    }

    val accent = ThemeState.accentColor
    Dialog(onDismissRequest = onDismiss, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Column(
            Modifier.fillMaxWidth(0.92f).fillMaxHeight(0.92f)
                .clip(RoundedCornerShape(18.dp)).background(PanelBg).padding(16.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Pilih Skin", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.weight(1f))
                Chip("SEGARKAN", RowBg, Color.White, enabled = !loading && busyId == null) { refreshKey++ }
                Spacer(Modifier.width(8.dp))
                Chip("TUTUP", accent, bestTextColorFor(accent), enabled = true) { onDismiss() }
            }
            Text(if (loading) "Memuat daftar…" else message, color = Dim, fontSize = 13.sp, modifier = Modifier.padding(vertical = 6.dp))
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.weight(1f)) {
                items(rows, key = { it.id }) { r ->
                    val isSel = r.id == selected
                    Row(
                        Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(RowBg)
                            .border(2.dp, if (isSel) accent else Color.Transparent, RoundedCornerShape(12.dp))
                            .padding(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Thumb(r)
                        Column(Modifier.weight(1f).padding(horizontal = 12.dp)) {
                            Text(r.title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
                            Text(r.sub, color = Dim, fontSize = 12.sp)
                            val st = when {
                                isSel -> "Sedang dipakai"
                                r.status == SkinRepository.Status.UPDATE -> "Ada pembaruan"
                                r.status == SkinRepository.Status.NOT_INSTALLED -> "Belum diunduh"
                                else -> ""
                            }
                            if (st.isNotEmpty()) Text(st, color = accent, fontSize = 12.sp)
                        }
                        val busy = busyId == r.id
                        val canUse = r.repo == null || r.status == SkinRepository.Status.INSTALLED
                        when {
                            busy -> Text("…", color = Dim, fontSize = 18.sp)
                            canUse && !isSel -> Chip("PAKAI", accent, bestTextColorFor(accent), enabled = busyId == null) { useId(r.id) }
                            !canUse -> Chip(
                                if (r.status == SkinRepository.Status.UPDATE) "PERBARUI" else "UNDUH", accent, bestTextColorFor(accent),
                                enabled = busyId == null && r.repo != null && r.repo.files.isNotEmpty()
                            ) { install(r.repo!!) }
                        }
                        if (r.status == SkinRepository.Status.UPDATE && r.repo != null && r.repo.files.isNotEmpty()) {
                            Spacer(Modifier.width(6.dp))
                            Chip("PAKAI", RowBg, Color.White, enabled = busyId == null && !isSel) { useId(r.id) }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun Thumb(r: SkinRow) {
    val context = LocalContext.current
    val bmp by produceState<ImageBitmap?>(null, r.id, r.status) {
        value = r.repo?.let { s ->
            SkinRepository.previewText(context, s)?.let { withContext(Dispatchers.IO) { renderThumb(it, 320, 144) } }
        }
    }
    Box(Modifier.width(160.dp).height(72.dp).clip(RoundedCornerShape(8.dp)).background(Color(0xFF0B0D12)), contentAlignment = Alignment.Center) {
        val b = bmp
        if (b != null) Image(b, null, Modifier.size(160.dp, 72.dp), contentScale = ContentScale.Fit)
        else Text(if (r.repo == null) "—" else "…", color = Dim, fontSize = 14.sp)
    }
}

@Composable
private fun Chip(text: String, bg: Color, fg: Color, enabled: Boolean, onClick: () -> Unit) {
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier.height(34.dp).clip(RoundedCornerShape(17.dp))
            .background(if (enabled) bg else bg.copy(alpha = 0.4f))
            .clickable(enabled = enabled, onClick = onClick).padding(horizontal = 16.dp)
    ) { Text(text, color = fg, fontSize = 12.sp, fontWeight = FontWeight.Bold) }
}

/** preview.svg -> bitmap kecil (AndroidSVG). null bila gagal; tidak pernah melempar. */
private fun renderThumb(svgText: String, w: Int, h: Int): ImageBitmap? = try {
    val svg = SVG.getFromString(svgText)
    svg.setDocumentWidth(w.toFloat())
    svg.setDocumentHeight(h.toFloat())
    val bmp = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
    svg.renderToCanvas(Canvas(bmp))
    bmp.asImageBitmap()
} catch (t: Throwable) { null }
