package com.karaoke.reverbmic.skin

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Pusat Skin Engine mixer. Rantai fallback: skin pilihan -> skin default (assets) -> UI klasik.
 * Skin rusak / gagal render -> pilihan di-reset ke UI klasik, state = Failed. Tidak crash.
 * Skin unduhan repo (SkinRepository, cache offline) dimuat lewat [resolveDownloadedDir].
 */
object SkinManager {
    private const val TAG = "SkinManager"

    sealed class State {
        object Loading : State()
        /** UI klasik (fallback permanen). */
        object Classic : State()
        data class Active(val skin: SkinDefinition) : State()
        data class Failed(val reason: String) : State()
    }

    const val CLASSIC_ID = "classic"
    /** Skin bawaan APK (assets/skins/default). */
    const val BUNDLED_ID = "default"
    /** Pilihan awal: skin default. Gagal dimuat/dirender -> UI klasik. */
    const val DEFAULT_ID = BUNDLED_ID

    private const val PREFS = "skin_prefs"
    private const val KEY_SELECTED = "selected_skin_id"

    @Volatile private var appContext: Context? = null
    @Volatile private var loadStarted = false

    var state: State by mutableStateOf<State>(State.Loading)
        private set

    fun selectedId(context: Context): String =
        context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .getString(KEY_SELECTED, DEFAULT_ID) ?: DEFAULT_ID

    private fun saveSelected(context: Context, id: String) {
        context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putString(KEY_SELECTED, id).apply()
    }

    suspend fun ensureLoaded(context: Context) {
        if (state !is State.Loading || loadStarted) return
        loadStarted = true
        val app = context.applicationContext
        appContext = app
        try {
            state = if (selectedId(app) == CLASSIC_ID) State.Classic else withContext(Dispatchers.IO) { loadSelected(app) }
        } finally {
            if (state is State.Loading) loadStarted = false
        }
    }

    private fun loadSelected(app: Context): State {
        val id = selectedId(app)
        val r = loadById(app, id)
        if (r is State.Active) return r
        Log.w(TAG, "skin '$id' gagal dimuat, mencoba skin default")
        if (id != BUNDLED_ID) {
            val d = loadById(app, BUNDLED_ID)
            if (d is State.Active) { saveSelected(app, BUNDLED_ID); return d }
        }
        saveSelected(app, CLASSIC_ID)
        return r
    }

    private fun loadById(app: Context, id: String): State = when (id) {
        CLASSIC_ID -> State.Classic
        BUNDLED_ID -> loadFrom { SkinLoader.loadFromAssets(app) }
        else -> {
            val dir = resolveDownloadedDir(app, id)
            if (dir == null) State.Failed("skin '$id' belum tersedia") else loadFrom { SkinLoader.loadFromDir(dir) }
        }
    }

    /** Skin terunduh dari repo (cache offline); null bila belum terpasang / id tidak valid. */
    private fun resolveDownloadedDir(app: Context, id: String): java.io.File? = SkinRepository.cachedSkinDir(app, id)

    /** Pakai pilihan [id] (CLASSIC_ID, BUNDLED_ID, atau skin terunduh). true bila aktif; gagal -> pilihan sebelumnya tetap. */
    suspend fun useSkin(context: Context, id: String): Boolean {
        val app = context.applicationContext
        appContext = app
        return withContext(Dispatchers.IO) {
            val r = loadById(app, id)
            if (r is State.Active || r is State.Classic) { saveSelected(app, id); state = r; true } else false
        }
    }

    /** Muat + validasi; tidak pernah melempar. */
    fun loadFrom(loader: () -> SkinDefinition): State {
        return try {
            val skin = loader()
            val v = SkinValidator.validate(skin)
            v.warnings.forEach { Log.w(TAG, "peringatan skin '${skin.name}': $it") }
            if (v.ok) {
                Log.i(TAG, "skin '${skin.name}' v${skin.version} aktif (${skin.controls.size} kontrol, ${skin.source})")
                State.Active(skin)
            } else {
                Log.e(TAG, "skin '${skin.name}' ditolak: ${v.summary()}")
                State.Failed(v.summary())
            }
        } catch (e: Throwable) {
            Log.e(TAG, "skin gagal dimuat", e)
            State.Failed(e.message ?: e.javaClass.simpleName)
        }
    }

    /** Dipanggil SkinHost bila render fatal (OOM / AndroidSVG gagal): skin bawaan, bila itu pun gagal -> UI klasik. */
    fun reportRenderFailure(reason: String) {
        Log.e(TAG, "render skin gagal: $reason")
        val app = appContext
        if (app != null) {
            val sel = selectedId(app)
            // rantai fallback: skin terunduh -> skin default (assets) -> UI klasik
            if (sel != BUNDLED_ID && sel != CLASSIC_ID) {
                val d = loadById(app, BUNDLED_ID)
                if (d is State.Active) { saveSelected(app, BUNDLED_ID); state = d; return }
            }
            saveSelected(app, CLASSIC_ID)
        }
        state = State.Failed(reason)
    }
}
